import uuid
import bcrypt

from tortoise.transactions import in_transaction

from pydantic import constr
from pydantic.main import BaseModel

from fastapi import APIRouter
from fastapi.requests import Request

from user.db.rdb.schema import User, Agree, SnsType
from user.utils.validator import valid_phone
from user.utils.token import get_refresh_token, get_access_token

from common.config.consts import PASSWORD_REGEX
from common.models import SignInResponse
from common.db.rdb.schema import Error
from common.utils.excetions import SignupException


router = APIRouter()


class SignupPhoneRequest(BaseModel):
    phone: str
    password: constr(regex=PASSWORD_REGEX)
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    is_terms_of_service: bool
    is_privacy_statement: bool


@router.post('/phone', status_code=201, summary='휴대전화 가입 API', response_model=SignInResponse)
async def signup_phone_v1(request: Request, user_info: SignupPhoneRequest):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 휴대전화 가입 API

    # Request Body
    - phone: string =  국가코드 포함한 휴대폰 번호
    - password: string = 비밀번호
        - 정규식 검사 : 8자리 이상 + 숫자 + 특수문자
        - 유효성 검사 탈락시 422
    - first_name: string = 성
    - last_name: string = 이름
    - is_terms_of_service: boolean = 이용약관 동의 여부
    - is_privacy_statement: boolean = 개인정보취급방침 동의 여부

    # Error
    - 4000002 : 유효한 전화번호 아님
    - 4000003 : 중복된 전화번호
    - 4000004 : 모든 약관에 동의하지 않을시

    # Response
    - access_token: string = 액세스 토큰
        - 기본 유효기간 6시간
    - refresh_token: string = 리프레시 토큰
        - 기본 유효기간 14일
    - expired_date: datetime = 액세스 토큰 만료시점 (timezone : UTC)
    '''
    phone = await valid_phone(phone=user_info.phone)

    password = user_info.password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

    user_key = str(uuid.uuid4())
    refresh_token = get_refresh_token(user_key=user_key)

    if not user_info.is_privacy_statement or not user_info.is_terms_of_service:
        e = await Error.get(code = '4000004')
        raise SignupException(e=e)

    async with in_transaction():
        user = await User.create(
            user_key = user_key,
            phone = phone,
            password = hashed_pw,
            refresh_token = refresh_token,
            first_name = user_info.first_name,
            last_name = user_info.last_name,
        )

        await Agree.create(
            user=user,
            is_terms_of_service=user_info.is_terms_of_service,
            is_privacy_statement=user_info.is_privacy_statement
        )

        await SnsType.create(
            user=user,
            type='PHONE'
        )

    access_token, expired_date = get_access_token(user=user)

    return SignInResponse(
        access_token=f'Bearer {access_token}',
        refresh_token=f'Bearer {refresh_token}',
        expired_date=expired_date
    )
