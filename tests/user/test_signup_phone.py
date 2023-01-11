import anyio
from common.db.rdb.schema import Error

URI = '/api/v1/user/signup/phone'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=400, code='4000002'),
            Error(status_code=400, code='4000003'),
            Error(status_code=400, code='4000004')
        ])

    portal.call(create_test_suite)


def test_signup_phone_pass(client):
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

