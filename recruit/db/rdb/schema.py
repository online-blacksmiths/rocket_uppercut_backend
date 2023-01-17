from tortoise import fields
from tortoise.models import Model

from common.db.rdb.schema import BaseColumn


class Position(Model, BaseColumn):
    code = fields.CharField(max_length=30, unique=True)
    name = fields.CharField(max_length=100)

    class Meta:
        table = 'positions'

    def __str__(self):
        return self.code


class Skill(Model, BaseColumn):
    code = fields.CharField(max_length=30, unique=True)
    name = fields.CharField(max_length=200)

    class Meta:
        table = 'skills'

    def __str__(self):
        return self.code


class Company(Model, BaseColumn):
    code = fields.CharField(max_length=30, unique=True)
    name = fields.CharField(max_length=100)
    website = fields.CharField(max_length=255, default='')
    address = fields.CharField(max_length=250, default='')
    lat_x = fields.DecimalField(max_digits=14, decimal_places=10, default=37.49795982793813)
    lng_y = fields.DecimalField(max_digits=14, decimal_places=10, default=127.0276597140523)
    description = fields.TextField(default='')

    class Meta:
        table = 'companies'

    def __str__(self):
        return self.code
