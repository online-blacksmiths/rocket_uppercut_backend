from redis_om import HashModel


class Refresh(HashModel):
    refresh_token: str
