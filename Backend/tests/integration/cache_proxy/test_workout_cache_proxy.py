import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.workout import Workout
from Backend.schemas.workout import ListWorkoutResponse, WorkoutGetAllFilter, WorkoutUpdate
from Backend.services.WorkoutService import WorkoutService

from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.utils.uow import UnitOfWork

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutCachyProxy:

    @pytest.fixture
    def service(self, uow: UnitOfWork, redis: Redis):
        return WorkoutCacheProxy(uow=uow, redis=redis)

    async def test_get_all_workouts_cache(
        self,
        service: WorkoutCacheProxy,
        db_session: AsyncSession,
        workout: Workout
    ):
        redis = service.redis

        data = WorkoutGetAllFilter(
            skip=0,
            limit=50,
            user_id=workout.user_id
        )
        await service.get_all_workouts(user_id=workout.user_id, data=data)
        
        caches = [key async for key in redis.scan_iter(match="workouts:all:*")]

        assert len(caches) > 0

        await db_session.delete(workout)

        cache_result = await service.get_all_workouts(user_id=workout.user_id, data=data)

        assert cache_result is not None
        assert isinstance(cache_result, (str, bytes))

    async def test_get_loaded_workout_cache(
        self,
        service: WorkoutCacheProxy,
        workout: Workout
    ):
        await service.get_loaded_workout(
            workout_id=workout.id,
            user_id=workout.user_id
        )

        cache_result = await service.get_loaded_workout(
            workout_id=workout.id,
            user_id=workout.user_id
        )
        
        assert cache_result is not None
        assert isinstance(cache_result, (str, bytes))

    async def test_update_workout_invalidate_cache(
        self,
        service: WorkoutCacheProxy,
        workout: Workout
    ):
        redis: Redis = service.redis

        await service.get_loaded_workout(
            workout_id=workout.id,
            user_id=workout.user_id
        )
        data = WorkoutGetAllFilter(
            skip=0, 
            limit=50, 
            user_id=workout.user_id,
            public=None
        )
        await service.get_all_workouts(
            user_id=workout.user_id,
            data=data
        )

        cache_all_workouts = [
            key 
            async for key in redis.scan_iter(
                match="workouts:all:*"
            )
        ]
        cache_loaded_workout = [
            key
            async for key in redis.scan_iter(
                match="loaded_workout:*"
            )
        ]

        assert len(cache_all_workouts) > 0
        assert len(cache_loaded_workout) > 0

        data = WorkoutUpdate(name="dump") 

        await service.update_workout(
            user_id=workout.user_id,
            workout_id=workout.id,
            data=data
        )

        cache_all_workouts_new_version_workouts = [
            key 
            async for key in redis.scan_iter(
                match="workouts:version:*"
            )
        ]
        cache_loaded_workout = [
            key
            async for key in redis.scan_iter(
                match="loaded_workout:*"
            )
        ]

        assert len(cache_all_workouts_new_version_workouts) > 0
        assert len(cache_loaded_workout) == 0

