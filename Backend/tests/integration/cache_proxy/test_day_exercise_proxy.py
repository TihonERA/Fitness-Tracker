import pytest

from Backend.cache_proxies.DayExerciseCacheProxy import DayExerciseCacheProxy
from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.models.workout import Workout
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseCreateDTO

@pytest.mark.asyncio(loop_scope="session")
class TestDayExerciseProxy:
    
    async def test_create_day_exercise(
        self, 
        day_exercise_proxy: DayExerciseCacheProxy, 
        workout_proxy: WorkoutCacheProxy,
        workout: Workout
    ):
        redis = day_exercise_proxy.redis

        day_id = workout.training_days[0].id
        data = DayExerciseCreate(
            exercise_order=10,
            exercise_id=3,
        )

        await workout_proxy.get_loaded_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        match = "loaded_workout:*"

        assert len([key async for key in redis.scan_iter(match=match)]) > 0


        await day_exercise_proxy.create_day_exercise(
            user_id=workout.user_id,
            workout_id=workout.id,
            day_id=day_id,
            data=data
        )

        assert len([key async for key in redis.scan_iter(match=match)]) == 0

    async def test_delete_day_exercise(
        self,
        day_exercise_proxy: DayExerciseCacheProxy,
        workout_proxy: WorkoutCacheProxy,
        workout: Workout
    ):
        redis = day_exercise_proxy.redis

        day_id = workout.training_days[0].id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        await workout_proxy.get_loaded_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        match = "loaded_workout:*"

        assert len([key async for key in redis.scan_iter(match=match)]) > 0

        await day_exercise_proxy.delete_day_exercise(
            user_id=workout.user_id, 
            workout_id=workout.id,
            day_id=workout.training_days[0].id,
            exercise_id=exercise_id
        )

        assert len([key async for key in redis.scan_iter(match=match)]) == 0

