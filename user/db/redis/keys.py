from redis_om import HashModel, Field

from user.db.rdb.schema import StepTypeEnum


class Step(HashModel):
    type: StepTypeEnum
    step_1: bool = Field(default=False)
    step_2: bool = Field(default=False)
    step_3: bool = Field(default=False)

