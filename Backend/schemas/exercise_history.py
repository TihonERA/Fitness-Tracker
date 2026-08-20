from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from .base import OptionalInt

class SetsHistory(BaseModel):
    set: int | None = None
    reps: int | None = None
    weight: float | None = None
    time_for_set: datetime | None = None

class ExerciseHistoryCreate(BaseModel):
    exercise_id: int
    training_day_history_id: OptionalInt
    sets_history: list[SetsHistory] = []

class ExerciseHistoryCreateDTO(ExerciseHistoryCreate):
    user_id: UUID 
    
