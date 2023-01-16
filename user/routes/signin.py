import bcrypt
from pydantic.main import BaseModel

from fastapi import APIRouter
from fastapi.requests import Request

from common.utils.exceptions import SignInError
from common.models import SignInResponse
from common.db.rdb.schema import Error

from user.db.rdb.schema import User, SnsTypeEnum
from user.utils.token import get_refresh_token, get_access_token
from user.utils.validator import get_user_type


router = APIRouter()


class LoginRequest(BaseModel):
    ci: str
    password: str


@router.post('', status_code=201, summary='로그인 API', response_model=SignInResponse)
async def signin_v1(request: Request, data: LoginRequest):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - Login API

    # Error
    - 4010005 : 로그인 실패

    # Request Body
    - ci: str = 휴대전화 (국가코드 제외) 또는 이메일
    - password: str = 비밀번호

    # Response
    - access_token: string = 액세스 토큰
        - 기본 유효기간 6시간
    - refresh_token: string = 리프레시 토큰
        - 기본 유효기간 14일
    - expired_date: datetime = 액세스 토큰 만료시점 (timezone : KST)
    '''
    user_type, ci = await get_user_type(request, data.ci)

    if user_type == SnsTypeEnum.EMAIL:
        user = await User.get_or_none(email=ci)

    elif user_type == SnsTypeEnum.PHONE:
        user = await User.get_or_none(phone=ci)

    if not user:
        e = await Error.get(code='4010005')
        raise SignInError(e=e)

    if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        e = await Error.get(code='4010005')
        raise SignInError(e=e)

    user.refresh_token = get_refresh_token(user_key=user.user_key)
    await user.save()

    access_token, expired_date = get_access_token(user=user)

    return SignInResponse(
        access_token=f'Bearer {access_token}',
        refresh_token=f'Bearer {user.refresh_token}',
        expired_date=expired_date
    )
