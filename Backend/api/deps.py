from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.WorkoutService import WorkoutService
from redis import Redis
from ..core.database import get_db, get_redis

def get_workout_service(db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    return WorkoutService(db=db, redis=redis)