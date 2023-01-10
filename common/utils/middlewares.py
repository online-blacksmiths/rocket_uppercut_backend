import uuid
import contextvars
import time
import traceback
import re
from datetime import datetime

import jwt
from loguru import logger

from fastapi import Request
from fastapi.responses import JSONResponse

from user.db.rdb.schema import User

from common.utils.excetions import exception_handler
from common.utils.excetions import LoginRequire, TokenExpired, TokenDecodeError
from common.config.consts import LOGIN_REQUIRED_PATH_LIST, LOGIN_REQUIRED_REGEX_PATH_LIST
from common.config.settings import conf
from common.db.rdb.schema import Error


request_id_contextvar = contextvars.ContextVar('request_id', default=None)


async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_contextvar.set(request_id)

    request.state.req_time = datetime.utcnow()
    request.state.start = time.time()

    logger.debug(f'Request Started : {request_id}')

    try:
        response = await call_next(request)
        return response

    except Exception as e:
        error = await exception_handler(e)
        error_data = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)

        logger.warning(str(error_data))

        if error.status_code == 500:
            logger.error(traceback.format_exc())

        response = JSONResponse(status_code=error.status_code, content=error_data)
        return response

    finally:
        assert request_id_contextvar.get() == request_id
        t = time.time() - request.state.start

        logger.debug(f'Request Ended : {request_id}')
        logger.info(f'Processed Time [{request_id}] : {str(round(t * 1000, 5))}ms')


async def access_control(request: Request, call_next):
    request.state.user = None
    headers = request.headers

    url = request.url.path

    try:
        if url != '/':
            if url in LOGIN_REQUIRED_PATH_LIST or url_check(url):
                if 'authorization' not in headers.keys():
                    e = await Error.get(code='4010001')
                    raise LoginRequire(e=e)

            if 'authorization' in headers.keys():
                token_info = await token_decode(access_token=headers.get('authorization'))

                request.state.user = await user_check(**token_info)

        response = await call_next(request)
        return response

    except Exception as e:
        error = await exception_handler(e)
        error_data = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)

        logger.warning(str(error_data))

        if error.status_code == 500:
            logger.error(traceback.format_exc())

        response = JSONResponse(status_code=error.status_code, content=error_data)
        return response


def url_check(path) -> bool:
    pattern = '(?:%s)' % '|'.join(LOGIN_REQUIRED_REGEX_PATH_LIST)
    result = re.match(pattern, path).group()

    if result == path:
        return True
    return False


async def token_decode(access_token) -> dict:
    try:
        access_token = access_token.replace('Bearer ', '')
        payload = jwt.decode(access_token, key=conf().JWT_SECRET, algorithms=[conf().ACCESS_JWT_ALGORITHM])

        return payload

    except jwt.ExpiredSignatureError:
        e = await Error.get(code = '4010002')
        raise TokenExpired(e = e)

    except jwt.DecodeError:
        e = await Error.get(code = '4010003')
        raise TokenDecodeError(e = e)


async def user_check(user_key, **kwargs) -> User:
    user = await User.get_or_none(user_key = user_key, is_delete=False)
    now = datetime.utcnow()

    if not user:
        e = await Error.get(code='4010001')
        raise LoginRequire(e=e)

    user.last_visit = now

    await user.save()
    return user
