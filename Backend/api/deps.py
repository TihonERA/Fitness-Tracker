from fastapi import Depends, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi import Query
from ..schemas.workout import WorkoutGetAllFilter
from ..services.WorkoutService import WorkoutService
from ..core.database import get_db, get_redis

IntPath = Annotated[int, Path()]

def get_workout_service(db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    return WorkoutService(db=db, redis=redis)

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
