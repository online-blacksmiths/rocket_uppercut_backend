from redis_om import HashModel, Field

from user.db.rdb.schema import StepTypeEnum


class Step(HashModel):
    type: StepTypeEnum
    step_1: int = Field(default=0)
    step_2: int = Field(default=0)
    step_3: int = Field(default=0)

