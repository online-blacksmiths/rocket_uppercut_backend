import anyio
import uuid
import bcrypt
from datetime import datetime, timedelta

from user.db.rdb.schema import User, Step, StepTypeEnum

from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/me/phone'


def test_db_create(client, portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=401, code='4010002'),
            Error(status_code=401, code='4010003'),
            Error(status_code=400, code='4000002'),
            Error(status_code=400, code='4000003'),
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


def test_pass(client, portal: anyio.abc.BlockingPortal):
    res = client.put(
        URI,
        headers=dict(authorization = f'Bearer {access_token}'),
        json=dict(phone='+8201012341235')
    )

    assert res.status_code == 200

    async def valid_user():
        user = await User.get(user_key = user_key)

        assert user.phone == '+821012341235'

        user.phone = '+821012341234'
        await user.save()

    portal.call(valid_user)


def test_unauthorization_fail(client, portal: anyio.abc.BlockingPortal):
    res = client.put(
        URI,
        json=dict(phone='+8201012341235')
    )

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'

    async def valid_user():
        user = await User.get(user_key = user_key)
        assert user.phone == '+821012341234'

    portal.call(valid_user)


def test_invalid_phone_fail(client, portal: anyio.abc.BlockingPortal):
    res = client.put(
        URI,
        headers=dict(authorization = f'Bearer {access_token}'),
        json=dict(phone='+82102984098120391092388')
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000002'

    async def valid_user():
        user = await User.get(user_key = user_key)
        assert user.phone == '+821012341234'

    portal.call(valid_user)


def test_duplicate_phone_fail(client, portal: anyio.abc.BlockingPortal):
    res = client.put(
        URI,
        headers=dict(authorization = f'Bearer {access_token}'),
        json=dict(phone='+821012341234')
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000003'

    async def valid_user():
        user = await User.get(user_key = user_key)
        assert user.phone == '+821012341234'

    portal.call(valid_user)
