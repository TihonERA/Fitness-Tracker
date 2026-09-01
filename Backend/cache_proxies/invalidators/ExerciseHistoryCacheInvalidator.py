import logging
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator
from Backend.cache_proxies.key_formatters.ExerciseHistoryCacheKeyFormatter import (
    ExerciseHistoryCacheKeyFormatter,
)
from Backend.utils.decorators import cache_invalidation_logger

logger = logging.Logger(__name__)


class ExerciseHistoryCacheInvalidator(
    BaseCacheInvalidator[ExerciseHistoryCacheKeyFormatter]
):
    def __init__(
        self, redis: Redis, formatter: ExerciseHistoryCacheKeyFormatter
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
        loaded_key = self.formatter.get_loaded_key(id)
        version_key = self.formatter.get_version_key(user_id)
        tag_key = self.formatter.get_tag_key(user_id)

        async with self.redis.pipeline() as pipe:
            pipe.delete(loaded_key)
            pipe.incr(version_key)
            pipe.srem(tag_key, loaded_key)

            await pipe.execute()
