from enum import Enum

from tortoise import fields
from tortoise.models import Model

from common.db.rdb.schema import BaseColumn


class SnsTypeEnum(str, Enum):
    PHONE = 'PHONE'
    EMAIL = 'EMAIL'

    def __str__(self):
        return self.value


class StepTypeEnum(str, Enum):
    PHONE = 'PHONE'
    EMAIL = 'EMAIL'

    def __str__(self):
        return self.value


class User(Model, BaseColumn):
    '''
    회원 테이블
    '''
    user_key = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=255, default='')
    phone = fields.CharField(max_length=50, default='')
    password = fields.TextField(default='')
    refresh_token = fields.TextField(default='')
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    last_visit = fields.DatetimeField(null=True, default=None)
    is_delete = fields.BooleanField(default=False, index=True)
    is_verified_phone = fields.BooleanField(default=False)
    is_verified_email = fields.BooleanField(default=False)

    class Meta:
        table = 'users'

    def __str__(self):
        return self.user_key


class Agree(Model, BaseColumn):
    '''
    유저 동의 항목
    '''
    user = fields.OneToOneField('models.User', related_name='agree', on_delete='CASCADE')
    is_terms_of_service = fields.BooleanField(default=False)
    is_privacy_statement = fields.BooleanField(default=False)

    class Meta:
        table = 'agrees'

    def __str__(self):
        return self.user.user_key


class SnsType(Model, BaseColumn):
    '''
    소셜 로그인 타입
    '''
    user = fields.ForeignKeyField('models.User', related_name='sns_type', on_delete='CASCADE')
    type = fields.CharEnumField(SnsTypeEnum, max_length=30)

    class Meta:
        table = 'sns_types'
        unique_together = ['user_id', 'type']

    def __str__(self):
        return self.user.user_key


class Step(Model, BaseColumn):
    '''
    인증, 프로필, 연결하기 스텝
    '''
    user = fields.OneToOneField('models.User', related_name='step', on_delete='CASCADE')
    type = fields.CharEnumField(StepTypeEnum, max_length=30)
    step_1 = fields.BooleanField(default=False)
    step_2 = fields.BooleanField(default=False)
    step_3 = fields.BooleanField(default=False)

    class Meta:
        table = 'steps'

    def __str__(self):
        return self.user.user_key

    @property
    def is_completion(self):
        return all([self.step_1, self.step_2, self.step_3])

    @property
    def to_redis(self):
        return dict(type=self.type, step_1=int(self.step_1), step_2=int(self.step_2), step_3=int(self.step_3))
