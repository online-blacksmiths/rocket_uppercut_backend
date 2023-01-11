from pydantic.main import BaseModel

from redis_om import NotFoundError

from fastapi import APIRouter, BackgroundTasks
from fastapi.requests import Request

from common.db.redis.keys import RedisType
from common.db.rdb.schema import Error
from user.db.rdb.schema import StepTypeEnum
from user.db.redis.keys import Step as StepCache

from common.tasks.redis import set_cache
from common.utils.excetions import StepNotFound


router = APIRouter()


class GetStepResponse(BaseModel):
    type: StepTypeEnum
    step_1: bool
    step_2: bool
    step_3: bool


@router.get('', status_code=200, summary='인증 및 프로필, 연결하기 스탭 API', response_model=GetStepResponse)
async def get_step(request: Request, background_tasks: BackgroundTasks):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - Step API
    - 로그인 필요 (Headers.Authorization)

    # Error
    - 4040002 : Step 데이터가 존재하지 않을때

    # Response
    - type: str = 진행사항 유형 (PHONE | EMAIL)
    - step_1: bool = step 1 진행여부
    - step_2: bool = step 2 진행여부
    - step_3: bool = step 3 진행여부
    '''
    try:
        user = request.state.user
        cache = StepCache.get(pk=f'{user.user_key}#{RedisType.STEP.value}')

        return GetStepResponse(**cache.dict())

    except NotFoundError:
        step = await user.step

        if not step:
            e = await Error.get(code = '4040002')
            raise StepNotFound(e=e)

        if not step.is_completion:
            background_tasks.add_task(
                set_cache,
                StepCache,
                pk=f'{user.user_key}#{RedisType.STEP.value}',
                expired=60 * 30,
                **step.to_redis
            )

        return GetStepResponse(**dict(step))
