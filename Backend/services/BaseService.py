from ..utils.uow import UnitOfWork
from ..utils.exceptions import NotFound

from typing import Any

from redis.asyncio import Redis

class BaseService:

    def __init__(
        self,
        uow: UnitOfWork,
        redis: Redis 
    ) -> None:
        self.uow = uow
        self.redis = redis

    @staticmethod
    def check_if_instaces_is_none_returning_tuple(*args: Any) -> tuple[Any, ...]:
        for instance in args:
            if instance is None:
                raise NotFound()
        return args
