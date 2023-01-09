from datetime import datetime
from pytz import timezone

from tortoise import fields
from tortoise.models import Model

from common.config.consts import TIMEZONE, DATETIME_FORMAT

kst = timezone(TIMEZONE)


class BaseColumn:
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @property
    def created_at_kst(self):
        return datetime.strftime(self.created_at.astimezone(kst), DATETIME_FORMAT)

    @property
    def updated_at_kst(self):
        return datetime.strftime(self.updated_at.astimezone(kst), DATETIME_FORMAT)


class Error(Model, BaseColumn):
    '''
    Http Status 및 에러 메시지, 코드 테이블
    '''
    status_code = fields.IntField(index=True)
    msg = fields.CharField(max_length=300, default='')
    detail = fields.CharField(max_length=300, default='')
    code = fields.CharField(max_length=30, unique=True)

    class Meta:
        table = 'errors'

    def __str__(self):
        return self.code
