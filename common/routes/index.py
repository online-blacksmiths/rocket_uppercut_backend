import jwt
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from user.db.rdb.schema import User

from common.config.consts import DATETIME_FORMAT, AUTH_HEADER
from common.config.settings import conf


router = APIRouter()


@router.get('/', summary='Index & Healthcheck')
async def index():
    '''
    AWS Health Check
    '''

    current_time = datetime.utcnow()
    return Response(f"Rocket Uppercut API 🚀 (UTC : {current_time.strftime(DATETIME_FORMAT)})")


@router.get('/get_token', status_code=200)
async def get_token(user_key: str):
    user = await User.get(user_key = user_key)

    payload = dict(user_key=user.user_key)
    token = dict(Authorization=f"Bearer {create_token(payload=payload)}")

    return token


def create_token(*, payload: dict = None):
    token = jwt.encode(payload, key=conf().JWT_SECRET, algorithm=conf().ACCESS_JWT_ALGORITHM)

    return token


@router.get('/signin_test', status_code=200, dependencies=[Depends(AUTH_HEADER)])
async def signin_test(request: Request):
    return request.state.user.user_key
