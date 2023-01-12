import secrets
import string
from datetime import datetime, timedelta

from redis_om import NotFoundError

from pydantic.main import BaseModel
from pydantic import constr

from tortoise.transactions import in_transaction

from fastapi import APIRouter, BackgroundTasks
from fastapi.requests import Request

from user.tasks.send_verify_code_sms import task as send_sms_task
from user.db.redis.keys import Step as StepCache

from common.db.redis.keys import RedisType
from common.db.rdb.schema import Error
from common.db.mongodb.documents import TTLData, TTLTypeEnum

from common.tasks.redis import set_cache
from common.models import ResponseOK
from common.config.settings import conf
from common.config.consts import PHONE_VERIFY_CODE_REGEX
from common.utils.mongo_utils import get_or_none
from common.utils.exceptions import TooManyRequestVerify, VerifyMsgNotFound, StepNotFound


router = APIRouter()


@router.get('', summary='휴대전화 인증번호 요청 API', response_model=ResponseOK)
async def get_verify_code_v1(request: Request, background_tasks: BackgroundTasks):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 휴대전화 인증번호 요청 API
    - 로그인 필요 (Headers.Authorization)

    # Error
    - 4000005 : 요청 횟수 초과 (5분 내 5회 시도)
    '''

    user = request.state.user

    if get_or_none(TTLData, ttl_type=TTLTypeEnum.BLOCK, phone=user.phone):
        e = await Error.get(code='4000005')
        raise TooManyRequestVerify(e=e)

    verify_code = ''.join(secrets.choice(string.digits) for _ in range(6))

    TTLData.objects.create(
        ttl_type=TTLTypeEnum.VERIFIED_PHONE,
        expired_at=datetime.utcnow() + timedelta(minutes=3),
        verify_code=verify_code,
        phone=user.phone
    )

    if 5 <= TTLData.objects.filter(ttl_type=TTLTypeEnum.VERIFIED_PHONE, phone=user.phone).count():
        TTLData.objects.create(
            ttl_type=TTLTypeEnum.BLOCK,
            expired_at=datetime.utcnow() + timedelta(minutes=5),
            phone=user.phone
        )

    if not (conf().DEBUG or conf().TEST_MODE):
        background_tasks.add_task(send_sms_task, user=user, verify_code=verify_code)

    return ResponseOK()


class VerifyPhoneReqeust(BaseModel):
    verify_code: constr(regex=PHONE_VERIFY_CODE_REGEX)


@router.post('', summary='휴대전화 인증번호 확인 API', status_code=200, response_model=ResponseOK)
async def confirm_verify_code_v1(request: Request, background_tasks: BackgroundTasks, data: VerifyPhoneReqeust):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 휴대전화 인증번호 확인 API
    - 로그인 필요 (Headers.Authorization)

    # Error
    - 4040002 : Step 데이터가 없음
    - 4040003 : 인증번호 메시지가 없음

    # Request Body
    - verify_code: str = 인증번호
        - regex = ^[0-9]{6}$
    '''

    user = request.state.user

    received = (TTLData.objects
                .filter(ttl_type=TTLTypeEnum.VERIFIED_PHONE, phone=user.phone)
                .order_by('-created_at')
                .first())

    if not received:
        e = await Error.get(code = '4040003')
        raise VerifyMsgNotFound(e=e)

    step = await user.step

    if not step:
        e = await Error.get(code='4040002')
        raise StepNotFound(e=e)

    if data.verify_code == received.verify_code:
        async with in_transaction():
            user.is_verified_phone = True
            await user.save()

            step.step_1 = True
            await step.save()

        (TTLData.objects
         .filter(ttl_type__in=[TTLTypeEnum.VERIFIED_PHONE, TTLTypeEnum.BLOCK], phone=user.phone)
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

    return ResponseOK()
