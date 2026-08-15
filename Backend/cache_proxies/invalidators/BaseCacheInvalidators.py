from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.key_formatters.BaseCacheKeyFormatter import BaseCacheKeyFormatter

FormatterT = TypeVar("FormatterT", bound=BaseCacheKeyFormatter)

class BaseCacheInvalidator(Generic[FormatterT], ABC):
    def __init__(self, redis: Redis, formatter: FormatterT) -> None:
        self.redis = redis
        self.formatter = formatter

    @abstractmethod
    async def invalidate_all(self, **kwargs) -> None:
        pass
