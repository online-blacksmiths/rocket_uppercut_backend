from tortoise import fields
from tortoise.models import Model

from common.db.rdb.schema import BaseColumn


class Position(Model, BaseColumn):
    '''
    포지션 테이블
    '''
    code = fields.CharField(max_length=100, unique=True)
    title = fields.CharField(max_length=100)

    class Meta:
        table = 'positions'

    def __str__(self):
        return self.code


class Skill(Model, BaseColumn):
    '''
    분야, 관심분야, 스킬 테이블
    '''
    code = fields.CharField(max_length=100, unique=True)
    title = fields.CharField(max_length=200)
    sub_title = fields.CharField(max_length=200, default='', index=True)
    is_initial = fields.BooleanField(default=False, index=True)

    class Meta:
        table = 'skills'

    def __str__(self):
        return self.code


class Company(Model, BaseColumn):
    '''
    회사 테이블
    '''
    code = fields.CharField(max_length=100, unique=True)
    title = fields.CharField(max_length=100)
    website = fields.CharField(max_length=255, default='')
    address = fields.CharField(max_length=250, default='')
    lat_x = fields.DecimalField(max_digits=14, decimal_places=10, default=37.49795982793813)
    lng_y = fields.DecimalField(max_digits=14, decimal_places=10, default=127.0276597140523)
    description = fields.TextField(default='')

    class Meta:
        table = 'companies'

    def __str__(self):
        return self.code
