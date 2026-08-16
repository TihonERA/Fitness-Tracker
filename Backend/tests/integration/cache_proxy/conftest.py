import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.TrainingDayCacheProxy import TrainingDayCacheProxy
from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy
from Backend.cache_proxies.invalidators.TrainingDayCacheInvalidator import TrainingDayCacheInvalidator
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayCacheKeyFormatter import TrainingDayCacheKeyFormatter
from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter
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
def tr_day_proxy(uow: UnitOfWork, redis: Redis, workout_formatter, workout_invalidator):
    formatter = TrainingDayCacheKeyFormatter()
    invalidator = TrainingDayCacheInvalidator(redis=redis, formatter=formatter)
    service = TrainingDayService(uow=uow)
    return TrainingDayCacheProxy(
        service=service, 
        redis=redis, 
        invalidator=invalidator, 
        workout_invalidator=workout_invalidator, 
        formatter=formatter
    )

@pytest.fixture
def workout_proxy(uow: UnitOfWork, redis: Redis, workout_invalidator, workout_formatter):
    service = WorkoutService(uow=uow)
    return WorkoutCacheProxy(
        service=service, 
        redis=redis, 
        invalidator=workout_invalidator, 
        formatter=workout_formatter
    )
