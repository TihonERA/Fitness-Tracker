from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi import Query

from Backend.cache_proxies.DayExerciseCacheProxy import DayExerciseCacheProxy
from Backend.cache_proxies.TrainingDayCacheProxy import TrainingDayCacheProxy
from Backend.cache_proxies.UserCacheProxy import UserCacheProxy
from Backend.cache_proxies.invalidators.UserCacheInvalidator import UserCacheInvalidator
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator
from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import UserCacheKeyFormatter

from Backend.cache_proxies.WorkoutCacheProxy import WorkoutCacheProxy

from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter
from Backend.services.AuthService import AuthService
from Backend.services.DayExerciseService import DayExerciseService
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.services.UserService import UserService
from Backend.utils.exceptions import InvalidCredentials
from Backend.utils.uow import UnitOfWork
from Backend.schemas.workout import WorkoutGetAllFilter
from Backend.services.WorkoutService import WorkoutService
from Backend.core.database import async_session_factory
from Backend.core.config import settings

def get_redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

async def get_uow():
    uow = UnitOfWork(session_maker=async_session_factory)
    return uow

def get_user_proxy(
    uow=Depends(get_uow),
    redis=Depends(get_redis)
) -> UserCacheProxy:
    formatter = UserCacheKeyFormatter()
    invalidator = UserCacheInvalidator(formatter=formatter, redis=redis)
    service = UserService(uow)
    return UserCacheProxy(service=service, redis=redis, formatter=formatter, invalidator=invalidator)
def get_workout_cache_formatter() -> WorkoutCacheKeyFormatter:
    return WorkoutCacheKeyFormatter()

def get_workout_cache_invalidator(
    redis=Depends(get_redis),
    formatter=Depends(get_workout_cache_formatter)
) -> WorkoutCacheInvalidator:
    return WorkoutCacheInvalidator(formatter=formatter, redis=redis)

def get_workout_proxy(
    uow=Depends(get_uow),
    redis=Depends(get_redis),
    formatter=Depends(get_workout_cache_formatter),
    invalidator=Depends(get_workout_cache_invalidator)
) -> WorkoutCacheProxy:
    service = WorkoutService(uow)
    return WorkoutCacheProxy(service=service, redis=redis, formatter=formatter, invalidator=invalidator)

def get_training_day_proxy(
    uow=Depends(get_uow),
    redis=Depends(get_redis),
    workout_invalidator=Depends(get_workout_cache_invalidator)
) -> TrainingDayCacheProxy:
    service = TrainingDayService(uow)
    return TrainingDayCacheProxy(service=service, redis=redis, workout_invalidator=workout_invalidator)

def get_day_exercise_proxy(
    uow=Depends(get_uow),
    redis=Depends(get_redis),
    workout_invalidator=Depends(get_workout_cache_invalidator)
) -> DayExerciseCacheProxy:
    service = DayExerciseService(uow)
    return DayExerciseCacheProxy(service=service, redis=redis, workout_invalidator=workout_invalidator)

def get_auth_service(user_proxy=Depends(get_user_proxy)) -> AuthService:
    return AuthService(user_proxy=user_proxy)

def get_tr_day_history_service(
    uow=Depends(get_uow),
    redis=Depends(get_redis)
) -> TrainingDayHistoryService:
    return TrainingDayHistoryService(uow=uow, redis=redis)

def get_current_user(
    access_token: str | bytes | None = Cookie(None),
    auth_service: AuthService = Depends(get_auth_service)
) -> UUID:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    try:
        user_id = auth_service.get_current_user(token=access_token)
        return user_id
    except InvalidCredentials as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

GetCurrentUserDepends = Annotated[UUID, Depends(get_current_user)]

def get_workouts_filter(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=500)] = 50,
    user_id: Annotated[UUID | None, Query()] = None,
    public: Annotated[bool | None, Query()] = None
) -> WorkoutGetAllFilter:
    return WorkoutGetAllFilter(
        skip=skip,
        limit=limit,
        user_id=user_id,
        public=public
    )

UserProxyDepends = Annotated[UserCacheProxy, Depends(get_user_proxy)]
AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]
WorkoutProxyDepends = Annotated[WorkoutCacheProxy, Depends(get_workout_proxy)]
TrainingDayProxyDepends = Annotated[TrainingDayCacheProxy, Depends(get_training_day_proxy)]
TrDayHistoryServiceDepends = Annotated[TrainingDayHistoryService, Depends(get_tr_day_history_service)]

UUIDPath = Annotated[UUID, Path()]
IntPath = Annotated[int, Path()]
