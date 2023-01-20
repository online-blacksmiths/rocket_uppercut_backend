import anyio
import uuid
import bcrypt
import phonenumbers

from user.db.rdb.schema import User, Step, StepTypeEnum, SnsTypeEnum

from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/signin'


def test_db_create(client, portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010005'),
            Error(status_code=404, code='4040002')
        ])

        global user_key
        user_key = str(uuid.uuid4())

        country_code = 'KR'
        phone = phonenumbers.parse('01012341234', country_code)

        global password
        password = 'unittest123!@#'

        user = await User.create(
            user_key = user_key,
            phone = f'+{phone.country_code}{phone.national_number}',
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


def test_phone_pass(client, mock_get_ip, mock_get_country_code):
    mock_get_ip.return_value = '1.1.1.1'
    mock_get_country_code.return_value = 'KR'

    res = client.post(URI, json=dict(ci='01012341234', password=password))

    assert res.status_code == 201


def test_invalid_email_ci_fail(client):
    res = client.post(URI, json=dict(ci='unittesttest.com', password=password))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'


def test_invalid_phone_ci_fail(client, mock_get_ip, mock_get_country_code):
    mock_get_ip.return_value = '1.1.1.1'
    mock_get_country_code.return_value = 'KR'

    res = client.post(URI, json=dict(ci='123412341234123412341234', password=password))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'


def test_invalid_pw_fail(client):
    res = client.post(URI, json=dict(ci='unittest@test.com', password='invalid_pw'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010005'
