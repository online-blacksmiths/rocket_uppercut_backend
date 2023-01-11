from enum import Enum

from datetime import datetime
from pydantic.main import BaseModel


class RedisType(Enum):
    REFRESH = 'REFRESH'

    def __str__(self):
        return self.value


class ResponseOK(BaseModel):
    message: str = 'OK'


class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str
    expired_date: datetime
