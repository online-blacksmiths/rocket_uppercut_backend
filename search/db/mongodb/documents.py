from enum import Enum

from mongoengine import fields
from mongoengine.document import Document

from common.db.mongodb.documents import BaseField


class TotalSearchEnum(Enum):
    SKILL = 'SKILL'
    POSITION = 'POSITION'
    COMPANY = 'COMPANY'
    PEOPLE = 'PEOPLE'
    RECRUIT = 'RECRUIT'
    SCHOOL = 'SCHOOL'
    ANY = 'ANY'

    def __str__(self):
        return self.value


class TotalSearch(BaseField, Document):
    title = fields.StringField()
    sub_title = fields.StringField()
    type = fields.EnumField(TotalSearchEnum)
    code = fields.StringField()
    total_sort = fields.IntField(default=0)

    meta = {'collection': 'total_search'}
