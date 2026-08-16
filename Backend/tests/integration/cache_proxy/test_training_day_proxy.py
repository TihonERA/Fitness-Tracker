import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.models.workout import Workout

from Backend.cache_proxies.TrainingDayCacheProxy import TrainingDayCacheProxy
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO, TrainingDayUpdate
from Backend.services.TrainingDayService import TrainingDayService

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

    async def test_update_training_day(
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

        data = TrainingDayUpdate(name="new", day_order=1)

        await tr_day_proxy.update_training_day(
            user_id=workout.user_id, 
            workout_id=workout.id,
            day_id=workout.training_days[0].id,
            data=data
        )

        assert len([key async for key in redis.scan_iter(match=match)]) == 0

    async def test_delete_training_day(
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

        await tr_day_proxy.delete_training_day(
            user_id=workout.user_id, 
            workout_id=workout.id,
            day_id=workout.training_days[0].id
        )

        assert len([key async for key in redis.scan_iter(match=match)]) == 0

