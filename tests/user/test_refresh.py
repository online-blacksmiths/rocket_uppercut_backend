import anyio
import uuid
import jwt
from datetime import datetime, timedelta

from user.db.rdb.schema import User

from user.utils.token import get_refresh_token
from common.config.settings import conf
from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/refresh'


def get_exp_refresh_token(user_key: str) -> str:
    payload = dict(
        user_key=user_key,
        exp=datetime.utcnow() - timedelta(seconds=1)
    )

    token = jwt.encode(payload, conf().JWT_SECRET, algorithm=conf().REFRESH_JWT_ALGORITHM)

    return token


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=401, code='4010003'),
            Error(status_code=401, code='4010004'),
            Error(status_code=400, code='4000005')
        ])

        global user_key
        user_key = str(uuid.uuid4())

        global refresh_token
        refresh_token = get_refresh_token(user_key=user_key)

        await User.create(
            user_key = user_key,
            phone = '+821012341234',
            first_name = 'unit',
            last_name = 'test',
            refresh_token = refresh_token
        )

        global access_token
        access_token = create_token(payload=dict(user_key=user_key))

    portal.call(create_test_suite)


def test_refresh_pass(client):
    res = client.post(
        URI,
        json=dict(
            access_token = access_token,
            refresh_token = refresh_token
        )
    )

    assert res.status_code == 200
    assert res.json()['access_token'] != f'Bearer {access_token}'


def test_invalid_access_token_fail(client):
    res = client.post(
        URI,
        json=dict(
            access_token = 'test',
            refresh_token = refresh_token
        )
    )

    assert res.status_code == 401
    assert res.json()['code'] == '4010003'


def test_invalid_refresh_token_fail(client):
    res = client.post(
        URI,
        json=dict(
            access_token = access_token,
            refresh_token = 'test'
        )
    )

    assert res.status_code == 401
    assert res.json()['code'] == '4010003'


def test_expired_refresh_token_fail(client):
    res = client.post(
        URI,
        json=dict(
            access_token = access_token,
            refresh_token = get_exp_refresh_token(user_key=user_key)
        )
    )

    assert res.status_code == 401
    assert res.json()['code'] == '4010004'
