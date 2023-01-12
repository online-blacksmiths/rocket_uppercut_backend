import anyio
import uuid
from datetime import datetime, timedelta

from user.db.rdb.schema import User, Step, StepTypeEnum
from user.db.redis.keys import Step as StepCache
from common.db.redis.keys import RedisType
from common.db.mongodb.documents import TTLData, TTLTypeEnum
from common.db.rdb.schema import Error

from common.routes.index import create_token
from common.utils.mongo_utils import get_or_none

VERIFY_PHONE_URI = '/api/v1/user/verify/phone'
PHONE = '+821012341234'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=400, code='4000005'),
            Error(status_code=404, code='4040002'),
            Error(status_code=404, code='4040003'),
        ])

        global user_key
        user_key = str(uuid.uuid4())

        user = await User.create(
            user_key = user_key,
            phone = PHONE,
            first_name = 'unit',
            last_name = 'test',
        )

        await Step.create(user=user, type=StepTypeEnum.PHONE)

        global access_token
        access_token = create_token(payload=dict(user_key=user_key))

    portal.call(create_test_suite)


def test_verify_phone_pass(client):
    res = client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 200

    ttl = get_or_none(TTLData, phone=PHONE, ttl_type=TTLTypeEnum.VERIFIED_PHONE)
    now = datetime.utcnow()

    assert ttl is not None
    assert now < ttl.expired_at < now + timedelta(minutes=4)
    assert ttl.verify_code is not None

    TTLData.objects.all().delete()


def test_login_required_fail(client):
    invalid_access_token = create_token(payload=dict(user_key='invalid_user'))
    res = client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {invalid_access_token}'))

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'

    res = client.get(VERIFY_PHONE_URI)

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_req_limit_fail(client):
    for _ in range(5):
        client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    res = client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 400
    assert res.json()['code'] == '4000005'

    ttl = get_or_none(TTLData, phone=PHONE, ttl_type=TTLTypeEnum.BLOCK)
    now = datetime.utcnow()

    assert TTLData.objects.filter(phone=PHONE, ttl_type=TTLTypeEnum.VERIFIED_PHONE).count() == 5
    assert ttl is not None
    assert now < ttl.expired_at < now + timedelta(minutes=6)
    assert ttl.phone == PHONE

    TTLData.objects.all().delete()


def test_confirm_phone_pass(client, portal: anyio.abc.BlockingPortal):
    for _ in range(5):
        client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    ttl = TTLData.objects.filter(ttl_type=TTLTypeEnum.VERIFIED_PHONE, phone=PHONE).order_by('-created_at').first()

    data = {'verify_code': ttl.verify_code}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 200

    cached_step = StepCache.get(pk=f'{user_key}#{RedisType.STEP}')
    assert cached_step.step_1 == 1
    assert TTLData.objects.filter(phone=PHONE).count() == 0

    async def valid_step():
        step = await Step.get(user__user_key=user_key)
        assert step.step_1 is True

    portal.call(valid_step)

    cached_step.db().flushall()
    TTLData.objects.all().delete()


def test_confirm_phone_verify_code_regex_fail(client):
    data = {'verify_code': 'invalid_verify_code'}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 422

    data = {'verify_code': '1234567'}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 422

    data = {'verify_code': '12345'}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 422


def test_confirm_phone_unauthorization_fail(client):
    data = {'verify_code': '123456'}
    res = client.post(VERIFY_PHONE_URI, json=data)

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_confirm_no_step_data_fail(client, portal: anyio.abc.BlockingPortal):
    client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    async def delete_step():
        step = await Step.get(user__user_key=user_key)
        await step.delete()

    portal.call(delete_step)

    data = {'verify_code': '123456'}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 404
    assert res.json()['code'] == '4040002'

    async def set_step():
        await Step.create(user=await User.get(user_key=user_key), type=StepTypeEnum.PHONE)

    portal.call(set_step)


def test_confirm_no_receive_data_fail(client):
    client.get(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'))

    TTLData.objects.all().delete()

    data = {'verify_code': '123456'}
    res = client.post(VERIFY_PHONE_URI, headers=dict(authorization = f'Bearer {access_token}'), json=data)

    assert res.status_code == 404
    assert res.json()['code'] == '4040003'
