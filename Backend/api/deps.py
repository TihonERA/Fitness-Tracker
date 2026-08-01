from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi import Query

from Backend.services.AuthService import AuthService
from Backend.services.DayExerciseService import DayExerciseService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.services.UserService import UserService
from Backend.utils.exceptions import InvalidCredentials
from Backend.utils.uow import UnitOfWork
from ..schemas.workout import WorkoutGetAllFilter
from ..services.WorkoutService import WorkoutService
from ..core.database import async_session_factory, get_redis

async def get_uow():
    uow = UnitOfWork(
        session_maker=async_session_factory
    )
    async with uow:
        yield uow

def get_workout_service(
    uow = Depends(get_uow), 
    redis: Redis = Depends(get_redis)
) -> WorkoutService:
    return WorkoutService(uow=uow, redis=redis)

def get_training_day_service(
    uow = Depends(get_uow), 
    redis = Depends(get_redis)
) -> TrainingDayService:
    return TrainingDayService(uow=uow, redis=redis)

def get_day_exercise_service(
    uow = Depends(get_uow), 
    redis = Depends(get_redis)
) -> DayExerciseService:
    return DayExerciseService(uow=uow, redis=redis)

def get_auth_service(
    uow=Depends(get_uow),
    redis=Depends(get_redis)
) -> AuthService:
    return AuthService(uow=uow, redis=redis)

def get_user_service(
    uow=Depends(get_uow),
    redis=Depends(get_redis)
) -> UserService:
    return UserService(uow=uow, redis=redis)

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
    user_id_from_token: GetCurrentUserDepends,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=500)] = 50,
    my: Annotated[bool, Query()] = False,
    user_id: Annotated[UUID | None, Query()] = None,
    public: Annotated[bool | None, Query()] = None
) -> WorkoutGetAllFilter:
    if my:
        user_id = user_id_from_token
    elif user_id != user_id_from_token:
        public=True

    return WorkoutGetAllFilter(
        skip=skip,
        limit=limit,
        user_id=user_id,
        public=public
    )

WorkoutServiceDepends = Annotated[WorkoutService, Depends(get_workout_service)]
TrainingDayServiceDepends = Annotated[TrainingDayService, Depends(get_training_day_service)]
DayExerciseServiceDepends = Annotated[DayExerciseService, Depends(get_day_exercise_service)]
AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDepends = Annotated[UserService, Depends(get_user_service)]

UUIDPath = Annotated[UUID, Path()]
IntPath = Annotated[int, Path()]
