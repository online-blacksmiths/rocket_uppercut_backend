from datetime import datetime
from pydantic.main import BaseModel


class ResponseOK(BaseModel):
    message: str = 'OK'


class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str
    expired_date: datetime
