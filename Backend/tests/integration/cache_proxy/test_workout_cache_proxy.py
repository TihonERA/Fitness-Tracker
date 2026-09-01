from types import CoroutineType
from typing import Any, Callable
from pydantic import RootModel
import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import (
    WorkoutCacheKeyFormatter,
)

from Backend.tests.integration.cache_proxy.conftest import keys_func

from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import (
    WorkoutCacheInvalidator,
)
from Backend.models.workout import Workout
from Backend.schemas.workout import (
    ListWorkoutResponse,
    WorkoutGetAllFilter,
    WorkoutRelationsResponse,
    WorkoutUpdate,
)
from Backend.services.WorkoutService import WorkoutService

from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutCachyProxy:
    @pytest.fixture
    def proxy(self, uow: UnitOfWork, redis: Redis):
        formatter = WorkoutCacheKeyFormatter()
        invalidator = WorkoutCacheInvalidator(redis=redis, formatter=formatter)
        service = WorkoutService(uow=uow)
        return WorkoutCacheProxy(
            service=service, redis=redis, invalidator=invalidator, formatter=formatter
        )

    async def test_get_all_workouts_cache(
        self,
        proxy: WorkoutCacheProxy,
        db_session: AsyncSession,
        workout: Workout,
        get_all_workouts_keys: keys_func,
    ):
        data = WorkoutGetAllFilter(skip=0, limit=50, user_id=workout.user_id)
        await proxy.get_all_workouts(user_id=workout.user_id, data=data)

        assert len(await get_all_workouts_keys()) > 0

        await db_session.delete(workout)

        cache_result = await proxy.get_all_workouts(user_id=workout.user_id, data=data)

        assert cache_result is not None
        assert isinstance(cache_result, RootModel)

    async def test_get_loaded_workout_cache(
        self, proxy: WorkoutCacheProxy, db_session: AsyncSession, workout: Workout
    ):
        await proxy.get_loaded_workout(workout_id=workout.id, user_id=workout.user_id)

        await db_session.delete(workout)

        cache_result = await proxy.get_loaded_workout(
            workout_id=workout.id, user_id=workout.user_id
        )

        assert cache_result is not None
        assert isinstance(cache_result, WorkoutRelationsResponse)

    async def test_update_workout_invalidate_cache(
        self,
        proxy: WorkoutCacheProxy,
        workout: Workout,
        get_loaded_workouts_keys: keys_func,
        get_all_workouts_keys: keys_func,
    ):
        await proxy.get_loaded_workout(workout_id=workout.id, user_id=workout.user_id)
        data = WorkoutGetAllFilter(
            skip=0, limit=50, user_id=workout.user_id, public=None
        )
        await proxy.get_all_workouts(user_id=workout.user_id, data=data)

        assert len(await get_all_workouts_keys()) > 0
        assert len(await get_loaded_workouts_keys()) > 0

        data = WorkoutUpdate(name="dump")

        await proxy.update_workout(
            user_id=workout.user_id, workout_id=workout.id, data=data
        )

        assert len(await get_all_workouts_keys()) > 0
        assert len(await get_loaded_workouts_keys()) == 0
