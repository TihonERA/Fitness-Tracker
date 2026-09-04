from typing import Any

from pydantic import BaseModel

from Backend.models.training_day_history import TrainingDayHistory
from Backend.schemas.base import BaseResponse, Str100
from Backend.schemas.exercise_history import (
    ExerciseHistoryBase,
    ExerciseHistoryCreate,
    SetsHistory,
)
from Backend.schemas.training_day_history import TrainingDayHistoryResponse


class ExerciseHistoryCreateNested(ExerciseHistoryBase):
    sets_history: list[SetsHistory] = []


class CreateHistory(BaseModel):
    day_name: Str100
    day_id: int
    exercises: list[ExerciseHistoryCreateNested] = []


class SetsDifference(BaseModel):
    reps: int | None = None
    weight: float | None = None


class ExerciseDifference(BaseModel):
    exercise_id: int | None = None
    sets_differences: list[SetsDifference] = []


class HistoryResponse(BaseResponse):
    last_training: TrainingDayHistoryResponse | None = None
    new_training: TrainingDayHistoryResponse
    differences: list[ExerciseDifference] = []
