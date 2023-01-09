import uuid
import contextvars
import time
import traceback
from datetime import datetime
from loguru import logger

from fastapi import Request
from fastapi.responses import JSONResponse

from common.utils.excetions import exception_handler


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
