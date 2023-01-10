import secrets
import string
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.requests import Request

from user.tasks.send_verify_code_sms import task as send_sms_task

from common.models import ResponseOK
from common.config.settings import conf
from common.config.consts import AUTH_HEADER
from common.utils.mongo_utils import get_or_none
from common.utils.excetions import TooManyRequestVerify
from common.db.rdb.schema import Error
from common.db.mongodb.documents import TTLData, TTLTypeEnum


router = APIRouter()


@router.get(
    '/phone',
    summary='휴대전화 인증번호 요청 API',
    response_model=ResponseOK,
    dependencies=[Depends(AUTH_HEADER)]
)
async def verify_phone_v1(request: Request, background_tasks: BackgroundTasks):
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
