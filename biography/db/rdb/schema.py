from enum import Enum

from tortoise import fields
from tortoise.models import Model

from common.db.rdb.schema import BaseColumn


class SchoolCategoryEnum(Enum):
    ELEMENTARY = '초등학교'
    MIDDLE = '중학교'
    HIGH = '고등학교'
    COLLEGE = '전문대학'
    UNIVERSITY = '대학'
    GRADUATE = '대학원'

    def __str__(self):
        return self.value


class School(Model, BaseColumn):
    '''
    학교 테이블
    '''
    title = fields.CharField(max_length=100)
    code = fields.CharField(max_length=100, unique=True)
    category = fields.CharEnumField(SchoolCategoryEnum, max_length=30)

    class Meta:
        table = 'schools'

    def __str__(self):
        return self.code


class Major(Model, BaseColumn):
    '''
    전공 테이블
    '''
    title = fields.CharField(max_length=100)
    code = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = 'majors'

    def __str__(self):
        return self.code
