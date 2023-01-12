import anyio
import uuid
import base64
from datetime import datetime, timedelta

from cryptography.fernet import Fernet

from user.db.rdb.schema import User, Step, StepTypeEnum
from user.db.redis.keys import Step as StepCache
from common.db.redis.keys import RedisType
from common.db.mongodb.documents import TTLData, TTLTypeEnum
from common.db.rdb.schema import Error

from common.config.settings import conf
from common.routes.index import create_token
from common.utils.mongo_utils import get_or_none

SEND_VERIFY_EMAIL_URI = '/api/v1/user/verify/email'
CONFIRM_EMAIL_URI = f'{SEND_VERIFY_EMAIL_URI}/confirm'
EMAIL = 'unittest@test.com'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=400, code='4000005'),
            Error(status_code=400, code='4000007'),
            Error(status_code=404, code='4040002'),
            Error(status_code=404, code='4040003'),
        ])

        global user_key
        user_key = str(uuid.uuid4())

        user = await User.create(
            user_key = user_key,
            email = EMAIL,
            first_name = 'unit',
            last_name = 'test',
        )

        await Step.create(user=user, type=StepTypeEnum.EMAIL)

        global access_token
        access_token = create_token(payload=dict(user_key=user_key))

    portal.call(create_test_suite)


def test_verify_email_pass(client):
    res = client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 200

    ttl = get_or_none(TTLData, email=EMAIL, ttl_type=TTLTypeEnum.VERIFIED_EMAIL)
    now = datetime.utcnow()

    assert ttl is not None
    assert now < ttl.expired_at < now + timedelta(minutes=6)

    TTLData.objects.all().delete()


def test_login_required_fail(client):
    invalid_access_token = create_token(payload=dict(user_key='invalid_user'))
    res = client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {invalid_access_token}'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'

    res = client.get(SEND_VERIFY_EMAIL_URI)

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_req_limit_fail(client):
    for _ in range(5):
        client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    res = client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 400
    assert res.json()['code'] == '4000005'

    ttl = get_or_none(TTLData, email=EMAIL, ttl_type=TTLTypeEnum.BLOCK)
    now = datetime.utcnow()

    assert TTLData.objects.filter(email=EMAIL, ttl_type=TTLTypeEnum.VERIFIED_EMAIL).count() == 5
    assert ttl is not None
    assert now < ttl.expired_at < now + timedelta(minutes=6)

    TTLData.objects.all().delete()


def test_no_email_fail(client, portal: anyio.abc.BlockingPortal):
    async def set_no_email():
        user = await User.get(user_key = user_key)
        user.email = ''
        await user.save()

    portal.call(set_no_email)

    res = client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 400
    assert res.json()['code'] == '4000007'

    async def set_email():
        user = await User.get(user_key = user_key)
        user.email = EMAIL
        await user.save()

    portal.call(set_email)


def test_confirm_email_pass(client, portal: anyio.abc.BlockingPortal):
    for _ in range(5):
        client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    fernet = Fernet(conf().ENCRYPT_KEY)
    encrypt_ci = base64.urlsafe_b64encode(fernet.encrypt(bytes(f'{user_key}|{EMAIL}', 'UTF-8'))).decode()

    res = client.get(f'{CONFIRM_EMAIL_URI}?ci={encrypt_ci}')

    assert res.status_code == 200

    cached_step = StepCache.get(pk=f'{user_key}#{RedisType.STEP}')
    assert cached_step.step_1 == 1
    assert TTLData.objects.filter(email=EMAIL).count() == 0

    async def valid_step():
        step = await Step.get(user__user_key=user_key)
        assert step.step_1 is True

    portal.call(valid_step)

    cached_step.db().flushall()
    TTLData.objects.all().delete()


def test_confirm_no_step_data_fail(client, portal: anyio.abc.BlockingPortal):
    client.get(SEND_VERIFY_EMAIL_URI, headers=dict(authorization = f'Bearer {access_token}'))

    fernet = Fernet(conf().ENCRYPT_KEY)
    encrypt_ci = base64.urlsafe_b64encode(fernet.encrypt(bytes(f'{user_key}|{EMAIL}', 'UTF-8'))).decode()

    async def delete_step():
        step = await Step.get(user__user_key=user_key)
        await step.delete()

    portal.call(delete_step)

    res = client.get(f'{CONFIRM_EMAIL_URI}?ci={encrypt_ci}')

    assert res.status_code == 404
    assert res.json()['code'] == '4040002'

    async def set_step():
        await Step.create(user=await User.get(user_key=user_key), type=StepTypeEnum.PHONE)

    portal.call(set_step)
