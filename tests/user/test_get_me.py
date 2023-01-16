import anyio
import uuid
import bcrypt
from datetime import datetime, timedelta

from user.db.rdb.schema import User, Step, StepTypeEnum

from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/me'


def test_db_create(client, portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=401, code='4010002'),
            Error(status_code=401, code='4010003'),
        ])

        global user_key
        user_key = str(uuid.uuid4())

        password = 'unittest123!@#'

        user = await User.create(
            user_key = user_key,
            phone = '+821012341234',
            email = 'unittest@test.com',
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            profile_img_url = 'test.com',
            first_name = 'unit',
            last_name = 'test',
            is_verified_phone = True
        )

        await Step.create(
            user=user,
            type=StepTypeEnum.PHONE
        )

        global access_token
        access_token = create_token(payload=dict(user_key=user_key))

    portal.call(create_test_suite)


def test_pass(client):
    res = client.get(URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 200

    res = res.json()
    assert res['phone'] == '+82 10-1234-1234'
    assert res['email'] == 'unittest@test.com'
    assert res['profile_img_url'] == 'test.com'
    assert res['is_verified_phone'] is True
    assert res['is_verified_email'] is False


def test_unauthorization_fail(client):
    res = client.get(URI)

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_token_expired_fail(client):
    token = create_token(payload=dict(user_key=user_key, exp=datetime.utcnow() - timedelta(hours=1)))

    res = client.get(URI, headers=dict(authorization = f'Bearer {token}'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010002'


def test_invalid_token_fail(client):
    res = client.get(URI, headers=dict(authorization = 'Bearer invalid_token'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010003'
