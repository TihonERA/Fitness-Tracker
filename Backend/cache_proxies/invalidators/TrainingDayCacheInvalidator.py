from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayCacheKeyFormatter import TrainingDayCacheKeyFormatter
from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter

class TrainingDayCacheInvalidator(BaseCacheInvalidator[TrainingDayCacheKeyFormatter]):
    def __init__(
        self, 
        redis: Redis,
        formatter: TrainingDayCacheKeyFormatter
    ) -> None:
        super().__init__(redis, formatter)

    async def invalidate_all(
        self,
        day_id: int
    ) -> None:
        loaded_tr_day_key = self.formatter.get_loaded_tr_day_key(day_id)

        await self.redis.delete(loaded_tr_day_key)
