import os
import anyio.abc
import pytest
from typing import Generator
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer
from mongoengine import disconnect, QuerySet

from main import create_app
from common.config.settings import conf
from common.config.tortoise import TORTOISE_ORM


@pytest.fixture(scope='module')
def client() -> Generator:
    os.environ['API_ENV'] = 'test'

    db_url = conf().TEST_DB_URL
    mongodb_url = conf().TEST_MONGO_DB_URL

    if conf().API_ENV != 'test':
        raise Exception("API_ENV must be 'test'")

    if not db_url or not mongodb_url:
        raise Exception('required DB_URL or MONGO_DB_URL')

    if db_url.split("@")[1].split("/")[0] != "localhost":
        raise Exception("db host must be 'localhost' in test environment")

    if db_url.split("/")[-1].split("?")[0].split("_")[0] != "test":
        raise Exception("schema name must start with 'test'")

    if mongodb_url.split("/")[3].split("?")[0].split("_")[0] != "test":
        raise Exception("mongo db must start with 'test'")

    initializer(
        modules=TORTOISE_ORM['apps']['models']['models'],
        db_url=db_url,
    )

    with TestClient(create_app()) as c:
        yield c
    finalizer()
    disconnect()


@pytest.fixture(scope="module")
def portal(client: TestClient) -> anyio.abc.BlockingPortal:
    assert client.portal
    return client.portal


@pytest.fixture(scope="function")
def mock_search(mocker):
    return mocker.patch.object(QuerySet, 'aggregate')


@pytest.fixture(scope="function")
def mock_get_ip(mocker):
    async_mock = MagicMock()
    mocker.patch('user.utils.validator.get_ip', side_effect=async_mock)

    return async_mock


@pytest.fixture(scope="function")
def mock_get_country_code(mocker):
    async_mock = MagicMock()
    mocker.patch('user.utils.validator.get_country_code', side_effect=async_mock)

    return async_mock
