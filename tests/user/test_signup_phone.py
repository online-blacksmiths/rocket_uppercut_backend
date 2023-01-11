import anyio

from common.db.redis.keys import RedisType
from common.db.rdb.schema import Error
from user.db.rdb.schema import User
from user.db.redis.keys import Step as StepCache

URI = '/api/v1/user/signup/phone'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=400, code='4000002'),
            Error(status_code=400, code='4000003'),
            Error(status_code=400, code='4000004')
        ])

    portal.call(create_test_suite)


def test_signup_phone_pass(client, portal: anyio.abc.BlockingPortal):
    res = client.post(
        URI,
        json={
            "phone": "+8201012341234",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 201

    async def cache_valid():
        user = await User.get(first_name='foo', last_name='bar')
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


def test_duplicate_phone_fail(client):
    res = client.post(
        URI,
        json={
            "phone": "+8201012341234",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000003'


def test_phone_number_too_long_fail(client):
    res = client.post(
        URI,
        json={
            "phone": "+82011123413542987194587198",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000002'


def test_invalid_phone_fail(client):
    res = client.post(
        URI,
        json={
            "phone": "+820001234",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000002'


def test_password_regex_valid_fail(client):
    res = client.post(
        URI,
        json={
            "phone": "+8201012351235",
            "password": "invalidpw",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 422


def test_disagree_fail(client):
    res = client.post(
        URI,
        json={
            "phone": "+8201038495039",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": False,
            "is_privacy_statement": False
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000004'

    res = client.post(
        URI,
        json={
            "phone": "+8201038495039",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": True,
            "is_privacy_statement": False
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000004'

    res = client.post(
        URI,
        json={
            "phone": "+8201038495039",
            "password": "unittest1234!",
            "first_name": "foo",
            "last_name": "bar",
            "is_terms_of_service": False,
            "is_privacy_statement": True
        }
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000004'

