import anyio
import uuid
import bcrypt

from user.db.rdb.schema import User, Step, StepTypeEnum

from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/signin'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010005'),
            Error(status_code=404, code='4040002')
        ])

        global user_key
        user_key = str(uuid.uuid4())

        global password
        password = 'unittest123!@#'

        user = await User.create(
            user_key = user_key,
            phone = '+821012341234',
            email = 'unittest@test.com',
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            first_name = 'unit',
            last_name = 'test',
        )

        await Step.create(
            user=user,
            type=StepTypeEnum.PHONE
        )

        global access_token
        access_token = create_token(payload=dict(user_key=user_key))

    portal.call(create_test_suite)


def test_email_pass(client):
    res = client.post(URI, json=dict(ci='unittest@test.com', password=password))

    assert res.status_code == 201


def test_phone_pass(client):
    res = client.post(URI, json=dict(ci='01012341234', password=password))

    assert res.status_code == 201


def test_invalid_email_ci_fail(client):
    res = client.post(URI, json=dict(ci='unittesttest.com', password=password))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'


def test_invalid_phone_ci_fail(client):
    res = client.post(URI, json=dict(ci='123412341234123412341234', password=password))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'


def test_invalid_pw_fail(client):
    res = client.post(URI, json=dict(ci='unittest@test.com', password='invalid_pw'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'
