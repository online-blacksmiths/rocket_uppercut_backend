from redis_om import HashModel


def set_cache(cls: HashModel, pk: str = None, expired: int = None, **kwargs) -> None:
    if expired:
        cls(pk=pk, **kwargs).save().expire(num_seconds=expired)

    cls(pk=pk, **kwargs).save()
