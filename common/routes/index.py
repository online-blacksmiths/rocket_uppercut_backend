import jwt
from datetime import datetime
import phonenumbers

from pydantic import EmailStr

from tortoise.expressions import Q

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from user.db.rdb.schema import User, Step, StepTypeEnum

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
async def get_token(user_key: str = None, email: EmailStr = None, phone: str = None):
    if not phone:
        phone = phonenumbers.parse(phone)
        phone = f'+{phone.country_code}{phone.national_number}'

    user = await User.filter(Q(user_key = user_key) | Q(email = email) | Q(phone = phone)).first()

    payload = dict(user_key=user.user_key)
    token = dict(Authorization=f"Bearer {create_token(payload=payload)}")

    return token


def create_token(*, payload: dict = None):
    token = jwt.encode(payload, key=conf().JWT_SECRET, algorithm=conf().ACCESS_JWT_ALGORITHM)

    return token


@router.get('/signin_test', status_code=200, dependencies=[Depends(AUTH_HEADER)])
async def signin_test(request: Request):
    return request.state.user.user_key


@router.post('/set_step', status_code=200)
async def set_step(user_key: str, step_1: bool, step_2: bool, step_3: bool, type: StepTypeEnum):
    user = await User.get_or_none(user_key = user_key)
    if not user:
        return Response("Not Found User")

    step = await user.step

    if not step:
        await Step.create(user=user, step_1=step_1, step_2=step_2, step_3=step_3, type=type)

    step.step_1 = step_1
    step.step_2 = step_1
    step.step_3 = step_1
    step.type = type

    await step.save()

    return Response('OK')


@router.delete('/del_user', status_code=204)
async def del_user(user_key: str):
    await User.filter(user_key = user_key).delete()

    return Response('OK')
