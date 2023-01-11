import jwt
import sys
import hashlib
import hmac
import base64
import time
from enum import Enum
from datetime import datetime, timedelta

from user.db.rdb.schema import User

from common.db.rdb.schema import Error
from common.config.settings import conf
from common.utils.excetions import TokenDecodeError, TokenExpired, UserNotFound


class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'

    def __str__(self):
        return self.value


def get_refresh_token(user_key: str) -> str:
    payload = dict(
        user_key=user_key,
        exp=datetime.utcnow() + timedelta(seconds=conf().REFRESH_EXP)
    )

    token = jwt.encode(payload, conf().JWT_SECRET, algorithm=conf().REFRESH_JWT_ALGORITHM)

    return token


def get_access_token(user: User) -> tuple[str, datetime]:
    payload = dict(
        user_key = user.user_key,
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        phone = user.phone,
        exp = datetime.utcnow() + timedelta(seconds=conf().ACCESS_EXP)
    )

    token = jwt.encode(payload, conf().JWT_SECRET, algorithm=conf().ACCESS_JWT_ALGORITHM)
    expired_date = payload['exp']

    return token, expired_date


async def valid_access_token(access_token: str) -> None:
    try:
        jwt.decode(access_token, key=conf().JWT_SECRET, algorithms=[conf().ACCESS_JWT_ALGORITHM])
        return None

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidSignatureError:
        e = await Error.get(code = '4010003')
        raise TokenDecodeError(e = e)

    except jwt.DecodeError:
        e = await Error.get(code = '4010003')
        raise TokenDecodeError(e = e)


async def valid_refresh_token(refresh_token: str) -> User:
    try:
        payload = jwt.decode(refresh_token, key=conf().JWT_SECRET, algorithms=[conf().REFRESH_JWT_ALGORITHM])

        user = await User.get_or_none(user_key = payload['user_key'])

        if not user:
            e = await Error.get(code='4040001')
            raise UserNotFound(e=e)

        return user

    except jwt.ExpiredSignatureError:
        e = await Error.get(code = '4010004')
        raise TokenExpired(e = e)

    except jwt.InvalidSignatureError:
        e = await Error.get(code = '4010003')
        raise TokenDecodeError(e = e)

    except jwt.DecodeError:
        e = await Error.get(code = '4010003')
        raise TokenDecodeError(e = e)


def get_ncp_signature(method: Method, url: str) -> tuple[str, str]:
    timestamp = str(int(time.time() * 1000))
    url = '/' + '/'.join(url.split('/')[3:])

    access_key = conf().NCP_ACCESS_KEY
    secret_key = bytes(conf().NCP_SECRET_KEY, 'UTF-8')

    method = str(method)
    message = bytes(f'{str(method)} {url}\n{timestamp}\n{access_key}', 'UTF-8')

    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return timestamp, signature
