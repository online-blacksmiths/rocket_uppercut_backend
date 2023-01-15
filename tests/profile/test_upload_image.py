import anyio
import uuid

from user.db.rdb.schema import User, Step, StepTypeEnum
from user.db.redis.keys import Step as StepCache
from common.db.redis.keys import RedisType

from common.config.consts import PROFILE_IMAGE_PATH
from common.config.settings import base_dir, conf
from common.routes.index import create_token
from common.db.rdb.schema import Error

URI = '/api/v1/profile/img'


def test_db_create(portal: anyio.abc.BlockingPortal):
    async def create_test_suite():
        await Error.bulk_create([
            Error(status_code=401, code='4010001'),
            Error(status_code=404, code='4040002'),
            Error(status_code=400, code='4000008'),
            Error(status_code=400, code='4000010')
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


def test_pass(client, portal: anyio.abc.BlockingPortal):
    file_name = base_dir + '/tests/mock/pass_img.jpeg'

    res = client.post(
        URI,
        files={'file': open(file_name, 'rb')},
        headers=dict(authorization = f'Bearer {access_token}')
    )

    assert res.status_code == 201

    async def check_user():
        user = await User.get(user_key=user_key)
        assert user.profile_img_url == f'{conf().FILE_SERVER_URL}/{PROFILE_IMAGE_PATH.replace("/web/", "")}/{user.user_key}.jpeg'

    portal.call(check_user)


def test_unauthorization_fail(client):
    file_name = base_dir + '/tests/mock/pass_img.jpeg'

    res = client.post(
        URI,
        files={'file': open(file_name, 'rb')},
    )

    assert res.status_code == 401
    assert res.json()['code'] == '4010001'


def test_big_size_img_fail(client):
    file_name = base_dir + '/tests/mock/over_200x200.jpeg'

    res = client.post(
        URI,
        files={'file': open(file_name, 'rb')},
        headers=dict(authorization = f'Bearer {access_token}')
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000008'


def test_not_support_format_fail(client):
    file_name = base_dir + '/tests/mock/test.txt'

    res = client.post(
        URI,
        files={'file': open(file_name, 'rb')},
        headers=dict(authorization = f'Bearer {access_token}')
    )

    assert res.status_code == 400
    assert res.json()['code'] == '4000010'
