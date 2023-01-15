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
    REDIS_URL: str = environ.get('REDIS_OM_URL', 'redis://@localhost:6379')
    DEBUG: bool = False
    TEST_MODE: bool = False
    JWT_SECRET: str = environ.get('JWT_SECRET')
    REFRESH_JWT_ALGORITHM: str = environ.get('REFRESH_JWT_ALGORITHM')
    ACCESS_JWT_ALGORITHM: str = environ.get('ACCESS_JWT_ALGORITHM')
    REFRESH_EXP: int = int(environ.get('REFRESH_EXP', 1209600))  # default: 14 Days
    ACCESS_EXP: int = int(environ.get('REFRESH_EXP', 21600))  # default: 6 Hours
    NCP_ACCESS_KEY: str = environ.get('NCP_ACCESS_KEY')
    NCP_SECRET_KEY: str = environ.get('NCP_SECRET_KEY')
    NCP_SENS_SERVICE_ID: str = environ.get('NCP_SENS_SERVICE_ID')
    ENCRYPT_KEY: bytes = bytes(environ.get('ENCRYPT_KEY', 'test'), 'UTF-8')
    EMAIL_VERIFY_URL: str = environ.get('EMAIL_VERIFY_URL', 'http://localhost:8000/api/v1/user/verify/email/confirm')
    FILE_SERVER_URL: str = environ.get('FILE_SERVER_URL', 'https://web.yongineer.cf')
    FILE_SERVER_IP: str = environ.get('FILE_SERVER_IP')
    FILE_SERVER_PORT: str = environ.get('FILE_SERVER_PORT')
    FILE_SERVER_USER: str = environ.get('FILE_SERVER_USER')
    FILE_SERVER_PW: str = environ.get('FILE_SERVER_PW')


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class DevConfig(Config):
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
    ENCRYPT_KEY: bytes = bytes('bw9YRccFBoFjGVlQUCK9HOJuUWJAwXr51y_zSBNHUJE=', 'UTF-8')


def conf():
    config = dict(local=LocalConfig, dev=DevConfig, prod=ProdConfig, test=TestConfig)

    return config[environ.get('API_ENV', 'local')]()
