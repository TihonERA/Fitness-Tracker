from abc import ABC, abstractmethod
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.CacheKeyFormatter import CacheKeyFormatter

class BaseCacheInvalidator(ABC):
    def __init__(self, redis: Redis, formatter: CacheKeyFormatter) -> None:
        self.redis = redis
        self.formatter = formatter

    @abstractmethod
    async def invalidate_all(self, **kwargs) -> None:
        pass
