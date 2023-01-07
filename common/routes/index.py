from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import Response

from common.config.consts import DATETIME_FORMAT

router = APIRouter()


@router.get('/')
async def index():
    '''
    AWS Health Check
    '''

    current_time = datetime.utcnow()
    return Response(f"Adoc API (UTC : {current_time.strftime(DATETIME_FORMAT)})")
