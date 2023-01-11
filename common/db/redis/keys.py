from enum import Enum


class RedisType(Enum):
    STEP = 'STEP'

    def __str__(self):
        return self.value

