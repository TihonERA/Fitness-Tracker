from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.WorkoutService import WorkoutService
from ..core.database import get_db

def get_workout_service(db: AsyncSession = Depends(get_db)):
    return WorkoutService(db=db)