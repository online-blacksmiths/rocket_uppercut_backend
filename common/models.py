from datetime import datetime
from pydantic.main import BaseModel


class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str
    expired_date: datetime
    is_verified_phone: bool
    is_verified_email: bool
