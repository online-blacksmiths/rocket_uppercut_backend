from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import Response

from common.config.consts import DATETIME_FORMAT
from common.db.rdb.schema import Error
from common.utils.excetions import InvalidData

router = APIRouter()


@router.get('/')
async def index():
    '''
    AWS Health Check
    '''

    current_time = datetime.utcnow()
    return Response(f"Rocket Uppercut API 🚀 (UTC : {current_time.strftime(DATETIME_FORMAT)})")


@router.get('/error')
async def error_test():
    '''
    에러 로깅 테스트용
    '''
    a = 1 / 0
    return a


@router.get('/error/handling')
async def handling_error_test():
    '''
    핸들링된 에러 테스트용
    '''

    e = await Error.get(code='4000001')
    raise InvalidData(e=e)
