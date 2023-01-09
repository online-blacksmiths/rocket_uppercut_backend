import jwt
from datetime import datetime, timedelta

from user.db.rdb.schema import User

from common.config.settings import conf


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
