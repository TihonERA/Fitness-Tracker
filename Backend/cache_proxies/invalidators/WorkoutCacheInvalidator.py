from functools import cache
import logging
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator

from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import (
    WorkoutCacheKeyFormatter,
)
from Backend.utils.decorators import cache_invalidation_logger

logger = logging.Logger(__name__)


class WorkoutCacheInvalidator(BaseCacheInvalidator[WorkoutCacheKeyFormatter]):
    def __init__(self, redis: Redis, formatter: WorkoutCacheKeyFormatter) -> None:
        super().__init__(redis, formatter)

    @cache_invalidation_logger(logger)
    async def invalidate_workouts_all(self, user_id: UUID) -> None:
        workouts_all_key_version = self.formatter.get_workouts_version_key(user_id)

        await self.redis.incr(workouts_all_key_version)

    @cache_invalidation_logger(logger)
    async def invalidate_loaded_workout(self, workout_id: int) -> None:
        loaded_workout_key = self.formatter.get_loaded_workout_key(workout_id)

        await self.redis.delete(loaded_workout_key)

    @cache_invalidation_logger(logger)
    async def invalidate_all(self, user_id: UUID, workout_id: int) -> None:
        loaded_workout_key = self.formatter.get_loaded_workout_key(workout_id)
        workouts_all_key_version = self.formatter.get_workouts_version_key(user_id)

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.incr(workouts_all_key_version)
            pipe.delete(loaded_workout_key)

            await pipe.execute()
