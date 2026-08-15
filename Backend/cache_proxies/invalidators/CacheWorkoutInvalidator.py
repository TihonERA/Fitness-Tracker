from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.CacheKeyFormatter import CacheKeyFormatter
from Backend.cache_proxies.invalidators.BaseCacheInvalidators import BaseCacheInvalidator 

from Backend.schemas.workout import WorkoutCachePrefixes


class CacheWorkoutInvalidator(BaseCacheInvalidator):
    def __init__(self, redis: Redis, formatter: CacheKeyFormatter) -> None:
        self.pref = WorkoutCachePrefixes
        super().__init__(redis, formatter)

    def _formate_workouts_all_key(self, user_id: UUID) -> str:
        workouts_all_key = self.formatter.formate_key(
            prefix=self.pref.version,
            user_id=user_id
        )
        return workouts_all_key

    def _formate_loaded_workout_key(
        self,
        user_id: UUID,
        workout_id: int
    ) -> str:
        loaded_workout_key = self.formatter.formate_key(
            prefix=self.pref.loaded_workout, 
            user_id=user_id,
            workout_id=workout_id
        )
        return loaded_workout_key

    async def invalidate_workouts_all(
        self,
        user_id: UUID
    ) -> None:
        workouts_all_key = self._formate_workouts_all_key(user_id=user_id)

        await self.redis.incr(workouts_all_key)

    async def invalidate_all(
        self,
        user_id: UUID,
        workout_id: int
    ) -> None:
        loaded_workout_key = self._formate_loaded_workout_key(
            user_id=user_id,
            workout_id=workout_id
        )
        workouts_all_key = self._formate_workouts_all_key(user_id)       

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.incr(workouts_all_key)
            pipe.delete(loaded_workout_key)

            await pipe.execute()

