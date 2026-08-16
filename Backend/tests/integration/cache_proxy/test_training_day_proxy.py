import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.models.workout import Workout

from Backend.cache_proxies.TrainingDayCacheProxy import TrainingDayCacheProxy
from Backend.cache_proxies.invalidators.TrainingDayCacheInvalidator import TrainingDayCacheInvalidator
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayCacheKeyFormatter import TrainingDayCacheKeyFormatter
from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.uow import UnitOfWork

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayCacheProxy:

    async def test_create_training_day(
        self,
        tr_day_proxy: TrainingDayCacheProxy,
        workout_proxy: WorkoutCacheProxy,
        workout: Workout
    ):
        redis = tr_day_proxy.redis

        await workout_proxy.get_loaded_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        match = "loaded_workout:*"

        assert len([key async for key in redis.scan_iter(match=match)]) > 0

        data = TrainingDayCreate(name="new", day_order=7)

        await tr_day_proxy.create_training_day(
            user_id=workout.user_id, 
            workout_id=workout.id,
            data=data
        )

        assert len([key async for key in redis.scan_iter(match=match)]) == 0
