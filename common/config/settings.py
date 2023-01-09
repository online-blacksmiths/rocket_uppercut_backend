from dataclasses import dataclass
from os import path, environ
from dotenv import load_dotenv

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv(dotenv_path=path.join(base_dir, '.env'))


@dataclass
class Config:
    API_ENV: str = environ.get("API_ENV", "local")
    PORT: int = int(environ.get("PORT", 8000))
    DB_URL: str = environ.get('DB_URL')
    MONGO_DB_URL: str = environ.get('MONGO_DB_URL')
    DEBUG: bool = False
    TEST_MODE: bool = False
    JWT_SECRET: str = environ.get('JWT_SECRET')
    REFRESH_JWT_ALGORITHM: str = environ.get('REFRESH_JWT_ALGORITHM')
    ACCESS_JWT_ALGORITHM: str = environ.get('ACCESS_JWT_ALGORITHM')
    REFRESH_EXP: int = int(environ.get('REFRESH_EXP', 1209600))  # default: 14 Days
    ACCESS_EXP: int = int(environ.get('REFRESH_EXP', 21600))  # default: 6 Hours


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = False


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True
    TEST_MODE: bool = True
    TEST_DB_URL: str = environ.get("TEST_DB_URL")
    TEST_MONGO_DB_URL: str = environ.get("TEST_MONGO_DB_URL")


def conf():
    config = dict(local=LocalConfig, prod=ProdConfig, test=TestConfig)

    return config[environ.get('API_ENV', 'local')]()
