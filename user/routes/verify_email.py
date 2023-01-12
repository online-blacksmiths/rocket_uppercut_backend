import base64
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from redis_om import NotFoundError

from tortoise.transactions import in_transaction

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from user.tasks.send_verify_email import task as verify_email

from user.db.rdb.schema import User
from user.db.redis.keys import Step as StepCache
from common.db.redis.keys import RedisType
from common.db.rdb.schema import Error
from common.db.mongodb.documents import TTLData, TTLTypeEnum

from common.tasks.redis import set_cache
from common.models import ResponseOK
from common.config.settings import conf
from common.config.consts import AUTH_HEADER, HOMEPAGE_URL
from common.utils.mongo_utils import get_or_none
from common.utils.exceptions import (
    TooManyRequestVerify, StepNotFound, InvalidData
)

router = APIRouter()


@router.get('', summary='인증 이메일 요청 API', response_model=ResponseOK, dependencies=[Depends(AUTH_HEADER)])
async def get_verify_email_v1(request: Request, background_tasks: BackgroundTasks):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 이메일 인증 요청 API
    - 로그인 필요 (Headers.Authorization)

    # Error
    - 4000007 : 이메일 정보 없음
    - 4000005 : 요청 횟수 초과 (5분 내 5회 시도)
    '''
    user = request.state.user

    if not user.email:
        e = await Error.get(code='4000007')
        raise InvalidData(e=e)

    if get_or_none(TTLData, ttl_type=TTLTypeEnum.BLOCK, email=user.email):
        e = await Error.get(code='4000005')
        raise TooManyRequestVerify(e=e)

    TTLData.objects.create(
        ttl_type=TTLTypeEnum.VERIFIED_EMAIL,
        expired_at=datetime.utcnow() + timedelta(minutes=5),
        email=user.email
    )

    if 5 <= TTLData.objects.filter(ttl_type=TTLTypeEnum.VERIFIED_EMAIL, email=user.email).count():
        TTLData.objects.create(
            ttl_type=TTLTypeEnum.BLOCK,
            expired_at=datetime.utcnow() + timedelta(minutes=5),
            email=user.email
        )

    fernet = Fernet(conf().ENCRYPT_KEY)
    encrypt_ci = base64.urlsafe_b64encode(fernet.encrypt(bytes(f'{user.user_key}|{user.email}', 'UTF-8'))).decode()

    if not (conf().DEBUG or conf().TEST_MODE):
        background_tasks.add_task(verify_email, user=user, ci=encrypt_ci)

    return ResponseOK()


@router.get('/confirm', summary='이메일 인증 확인 API', status_code=200)
async def confirm_verify_email_v1(request: Request, background_tasks: BackgroundTasks, ci: str):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 이메일 인증 확인 API
    - 유저가 이메일 메시지에서 [이메일 인증] 버튼 또는 인증 URL 클릭시 호출되는 API
    - 메인페이지로 리다이렉트 됨

    # Error
    - 4040002 : Step 데이터가 없음

    # Request Body
    - verify_code: str = 인증번호
        - regex = ^[0-9]{6}$
    '''
    fernet = Fernet(conf().ENCRYPT_KEY)
    decrypt_user_key, decrypt_email = fernet.decrypt(base64.urlsafe_b64decode(ci)).decode().split('|')

    user = await User.get(user_key = decrypt_user_key)
    step = await user.step

    if not step:
        e = await Error.get(code='4040002')
        raise StepNotFound(e=e)

    if user.email == decrypt_email:
        async with in_transaction():
            user.is_verified_email = True
            await user.save()

            step.step_1 = True
            await step.save()

        (TTLData.objects
         .filter(ttl_type__in=[TTLTypeEnum.VERIFIED_EMAIL, TTLTypeEnum.BLOCK], email=user.email)
         .delete())

    try:
        cached_step = StepCache.get(pk=f'{user.user_key}#{RedisType.STEP}')
        cached_step.update(step_1=1)

    except NotFoundError:
        background_tasks.add_task(
            set_cache,
            StepCache,
            pk=f'{user.user_key}#{str(RedisType.STEP)}',
            expired=60 * 30,
            **step.to_redis
        )

    return RedirectResponse(HOMEPAGE_URL)
