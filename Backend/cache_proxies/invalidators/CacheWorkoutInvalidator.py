from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidators import BaseCacheInvalidator 

from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter

class CacheWorkoutInvalidator(BaseCacheInvalidator[WorkoutCacheKeyFormatter]):
    def __init__(self, redis: Redis, formatter: WorkoutCacheKeyFormatter) -> None:
        super().__init__(redis, formatter)

    async def invalidate_workouts_all(
        self,
        user_id: UUID
    ) -> None:
        workouts_all_key_version = self.formatter.get_workouts_version_key(user_id)

        await self.redis.incr(workouts_all_key_version)

    async def invalidate_all(
        self,
        user_id: UUID,
        workout_id: int
    ) -> None:
        loaded_workout_key = self.formatter.get_loaded_workout_key(workout_id)
        workouts_all_key_version = self.formatter.get_workouts_version_key(user_id)       

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.incr(workouts_all_key_version)
            pipe.delete(loaded_workout_key)

            await pipe.execute()
