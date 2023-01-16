from phonenumbers import format_number, parse, PhoneNumberFormat

from pydantic.main import BaseModel
from pydantic import EmailStr

from fastapi import APIRouter
from fastapi.requests import Request


router = APIRouter()


class MeResponse(BaseModel):
    phone: str
    email: EmailStr
    profile_img_url: str
    is_verified_phone: bool
    is_verified_email: bool


@router.get('', status_code=200, summary='내 정보 API', response_model=MeResponse)
async def me(request: Request):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 내 정보 API
    - 로그인 필요 (Headers.Authorization)

    # Response
    - phone: str = 휴대폰 번호
    - email: str = 이메일 주소
    - profile_img_url: str = 프로필 이미지
    - is_verified_phone: boolean = 휴대폰 인증 여부
    - is_verified_email: boolean = 이메일 인증 여부
    '''
    user = request.state.user
    to_international_phone = format_number(parse(user.phone), PhoneNumberFormat.INTERNATIONAL)

    return MeResponse(
        phone = to_international_phone,
        email = user.email,
        profile_img_url = user.profile_img_url,
        is_verified_phone = user.is_verified_phone,
        is_verified_email = user.is_verified_email
    )
