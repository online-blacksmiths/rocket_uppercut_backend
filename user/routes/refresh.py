from pydantic.main import BaseModel

from fastapi import APIRouter, BackgroundTasks
from fastapi.requests import Request

from user.utils.token import valid_access_token, valid_refresh_token, get_access_token

from common.models import SignInResponse


router = APIRouter()


class RefreshRequest(BaseModel):
    access_token: str
    refresh_token: str


@router.post("", status_code=200, response_model=SignInResponse)
async def refresh(request: Request, background_tasks: BackgroundTasks, token_info: RefreshRequest):
    '''
    '''
    access_token = token_info.access_token.replace("Bearer ", "")
    refresh_token = token_info.refresh_token.replace("Bearer ", "")

    await valid_access_token(access_token=access_token)
    user = await valid_refresh_token(refresh_token=refresh_token)

    access_token, expired_date = get_access_token(user=user)

    return SignInResponse(access_token=access_token, refresh_token=refresh_token, expired_date=expired_date)
