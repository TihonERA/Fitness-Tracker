import asyncio
from functools import wraps
import logging

from types import CoroutineType
from typing import Any, Awaitable, Callable, Coroutine
from uuid import UUID


from redis import RedisError
from redis.asyncio import Redis

import json

import inspect

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayHistoryCacheKeyFormatter import (
    TrainingDayHistoryCacheKeyFormatter,
)
from Backend.utils.decorators import cache_invalidation_logger

logger = logging.getLogger(__name__)


class TrainingDayHistoryCacheInvalidator(
    BaseCacheInvalidator[TrainingDayHistoryCacheKeyFormatter]
):
    def __init__(
        self, redis: Redis, formatter: TrainingDayHistoryCacheKeyFormatter
    ) -> None:
        super().__init__(redis, formatter)

    @cache_invalidation_logger(logger)
    async def invalidate_loaded(self, id: int) -> None:
        loaded_key = self.formatter.get_loaded_key(id)

        await self.redis.delete(loaded_key)

    @cache_invalidation_logger(logger)
    async def invalidate_get_all(self, user_id: UUID) -> None:
        version_key = self.formatter.get_version_key(user_id)

        await self.redis.incr(version_key)

    @cache_invalidation_logger(logger)
    async def invalidate_all(self, user_id: UUID, id: int) -> None:
        tag_key = self.formatter.get_tag_key(user_id)
        loaded_key = self.formatter.get_loaded_key(id)
        version_key = self.formatter.get_version_key(user_id)

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.delete(loaded_key)
            pipe.srem(tag_key, loaded_key)
            pipe.incr(version_key)

            await pipe.execute()
