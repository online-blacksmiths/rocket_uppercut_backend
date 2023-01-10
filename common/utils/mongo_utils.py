from typing import Union
from mongoengine import DoesNotExist, Document, DynamicDocument


def get_or_none(cls: Union[Document, DynamicDocument], *args, **kwargs) -> Union[Document, DynamicDocument]:
    try:
        return cls.objects.get(*args, **kwargs)

    except DoesNotExist:
        return None
