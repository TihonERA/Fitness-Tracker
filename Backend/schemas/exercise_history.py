from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from .base import LimitInt, OptionalInt, SkipInt

class SetsHistory(BaseModel):
    set: int | None = None
    reps: int | None = None
    weight: float | None = None
    time_for_set: datetime | None = None

class ExerciseHistoryBase(BaseModel):
    exercise_id: int

class ExerciseHistoryCreate(ExerciseHistoryBase):
    training_day_history_id: OptionalInt
    sets_history: list[SetsHistory] = []

class ExerciseHistoryCreateDTO(ExerciseHistoryCreate):
    user_id: UUID 
    
class ExerciseHistoryGetAll(ExerciseHistoryBase):
    skip: SkipInt
    limit: LimitInt
    start_date: datetime | None = None
    end_date: datetime | None = None

class ExerciseHistoryGetAllDTO(ExerciseHistoryGetAll):
    user_id: UUID
