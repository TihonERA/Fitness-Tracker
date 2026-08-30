import asyncio
from types import CoroutineType
from typing import Any, Callable

from _pytest.config import print_conftest_import_error
import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.DayExerciseCacheProxy import DayExerciseCacheProxy
from Backend.cache_proxies.TrainingDayCacheProxy import TrainingDayCacheProxy
from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import (
    WorkoutCacheInvalidator,
)
from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import (
    WorkoutCacheKeyFormatter,
)
from Backend.schemas.workout import WorkoutCachePrefixes
from Backend.services.DayExerciseService import DayExerciseService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.services.WorkoutService import WorkoutService
from Backend.utils.uow import UnitOfWork


@pytest.fixture
def workout_formatter():
    return WorkoutCacheKeyFormatter()


@pytest.fixture
def workout_invalidator(redis, workout_formatter):
    return WorkoutCacheInvalidator(redis, workout_formatter)


@pytest.fixture
def day_exercise_proxy(uow: UnitOfWork, redis: Redis, workout_invalidator):
    service = DayExerciseService(uow=uow)
    return DayExerciseCacheProxy(
        service=service, redis=redis, workout_invalidator=workout_invalidator
    )


@pytest.fixture
def tr_day_proxy(uow: UnitOfWork, redis: Redis, workout_invalidator):
    service = TrainingDayService(uow=uow)
    return TrainingDayCacheProxy(
        service=service, redis=redis, workout_invalidator=workout_invalidator
    )


@pytest.fixture
def workout_proxy(
    uow: UnitOfWork, redis: Redis, workout_invalidator, workout_formatter
):
    service = WorkoutService(uow=uow)
    return WorkoutCacheProxy(
        service=service,
        redis=redis,
        invalidator=workout_invalidator,
        formatter=workout_formatter,
    )


@pytest.fixture
def get_loaded_workouts_keys(
    redis: Redis,
) -> Callable[[], CoroutineType[Any, Any, list[str | bytes]]]:
    match = WorkoutCachePrefixes.loaded_workout + ":*"

    async def _func():
        return [key async for key in redis.scan_iter(match=match)]

    return _func


@pytest.fixture
def get_all_workouts_keys(
    redis: Redis,
) -> Callable[[], CoroutineType[Any, Any, list[str | bytes]]]:
    match = WorkoutCachePrefixes.all_workouts + ":*"

    async def _func():
        return [key async for key in redis.scan_iter(match=match)]

    return _func


@pytest.fixture
def get_version_workouts_keys(
    redis: Redis,
) -> Callable[[], CoroutineType[Any, Any, list[str | bytes]]]:
    match = WorkoutCachePrefixes.version + ":*"

    async def _func():
        return [key async for key in redis.scan_iter(match=match)]

    return _func
