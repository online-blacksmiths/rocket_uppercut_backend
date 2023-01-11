import anyio
import uuid

from user.db.rdb.schema import User, Step, StepTypeEnum
from user.db.redis.keys import Step as StepCache
from common.db.redis.keys import RedisType

from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/user/verify/step'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=404, code='4040002')
        ])

        global user_key
        user_key = str(uuid.uuid4())

        user = await User.create(
            user_key = user_key,
            phone = '+821012341234',
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


def test_step_pass(client, portal: anyio.abc.BlockingPortal):
    res = client.get(URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 200

    res = res.json()
    assert res['type'] == 'PHONE'
    assert res['step_1'] is False
    assert res['step_2'] is False
    assert res['step_3'] is False

    async def cache_valid():
        user = await User.get(user_key = user_key)
        cache = StepCache.get(pk=f'{user.user_key}#{str(RedisType.STEP)}')
        expired = cache.db().pttl(cache.key())

        step = await user.step.values('type', 'step_1', 'step_2', 'step_3')

        assert 0 < (expired / (1000 * 60)) % 60 < 30
        assert cache.dict()['type'] == step['type']
        assert cache.dict()['step_1'] == int(step['step_1'])
        assert cache.dict()['step_2'] == int(step['step_2'])
        assert cache.dict()['step_3'] == int(step['step_3'])

        cache.db().flushall()

    portal.call(cache_valid)


def test_unauthrization_fail(client):
    res = client.get(URI)

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_step_not_found_fail(client, portal: anyio.abc.BlockingPortal):
    async def set_test_suite():
        await Step.all().delete()

    portal.call(set_test_suite)

    res = client.get(URI, headers=dict(authorization = f'Bearer {access_token}'))

    assert res.status_code == 404
    assert res.json()['code'] == '4040002'
