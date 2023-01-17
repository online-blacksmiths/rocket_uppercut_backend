from enum import Enum
from datetime import datetime

from mongoengine import fields
from mongoengine.document import DynamicDocument, Document


class BaseField:
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)


class TTLTypeEnum(Enum):
    BLOCK = 'BLOCK'
    VERIFIED_PHONE = 'VERIFIED_PHONE'
    VERIFIED_EMAIL = 'VERIFIED_EMAIL'


class TotalSearchEnum(Enum):
    SKILL = 'SKILL'
    POSITION = 'POSITION'
    COMPANY = 'COMPANY'


class TTLData(BaseField, DynamicDocument):
    expired_at = fields.DateTimeField()
    ttl_type = fields.EnumField(TTLTypeEnum, required=True)
    phone = fields.StringField()
    email = fields.EmailField()

    meta = {
        'collection': 'ttl_datas',
        'indexes': [
            'ttl_type',
            {'fields': ['expired_at'], 'expireAfterSeconds': 0},
        ]
    }


class TotalSearch(BaseField, Document):
    name = fields.StringField()
    type = fields.EnumField(TotalSearchEnum)
    code = fields.StringField()

    meta = {'collection': 'total_search'}
