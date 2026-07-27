from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi import Query

from Backend.services.AuthService import AuthService
from Backend.services.DayExerciseService import DayExerciseService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.validators import InvalidCredentials
from ..schemas.workout import WorkoutGetAllFilter
from ..services.WorkoutService import WorkoutService
from ..core.database import get_session, get_redis

def get_workout_service(session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)):
    return WorkoutService(session=session, redis=redis)

def get_training_day_service(session = Depends(get_session), redis = Depends(get_redis)):
    return TrainingDayService(session=session, redis=redis)

def get_day_exercise_service(session = Depends(get_session), redis = Depends(get_redis)):
    return DayExerciseService(session=session, redis=redis)

def get_auth_service(
    session=Depends(get_session),
    redis=Depends(get_redis)
) -> AuthService:
    return AuthService(session=session, redis=redis)

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

def get_workouts_filter(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=500),
    public: bool = Query(False)
) -> WorkoutGetAllFilter:
    return WorkoutGetAllFilter(
        skip=skip,
        limit=limit,
        public=public
    )

WorkoutServiceDepends = Annotated[WorkoutService, Depends(get_workout_service)]
TrainingDayServiceDepends = Annotated[TrainingDayService, Depends(get_training_day_service)]
DayExerciseServiceDepends = Annotated[DayExerciseService, Depends(get_day_exercise_service)]
AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]

IntPath = Annotated[int, Path()]
