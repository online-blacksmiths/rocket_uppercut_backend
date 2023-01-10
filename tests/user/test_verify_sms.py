import anyio
import uuid
from datetime import datetime, timedelta

from user.db.rdb.schema import User

from common.routes.index import create_token
from common.utils.mongo_utils import get_or_none
from common.db.mongodb.documents import TTLData, TTLTypeEnum
from common.db.rdb.schema import Error

VERIFY_PHONE_URI = '/api/v1/verify/phone'
PHONE = '+821012341234'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=400, code='4000005')
        ])

        global user_key
        user_key = str(uuid.uuid4())

        await User.create(
            user_key = user_key,
            phone = PHONE,
            first_name = 'unit',
            last_name = 'test',
        )

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
