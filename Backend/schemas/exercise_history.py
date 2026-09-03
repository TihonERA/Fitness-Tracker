from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, RootModel
from .base import BaseResponse, LimitInt, OptionalInt, SkipInt


class SetsHistory(BaseModel):
    set: int | None = None
    reps: int | None = None
    weight: float | None = None
    time_for_set: datetime | None = None


class ExerciseHistoryBase(BaseModel):
    exercise_id: int


class ExerciseHistoryResponse(BaseResponse, ExerciseHistoryBase):
    created_at: datetime


class ExerciseHistoryRelalationsResponse(ExerciseHistoryResponse):
    sets_history: list[SetsHistory] = []


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


class ExerciseHistoryCachePrefixes(StrEnum):
    tag = "eh_tag"
    loaded = "eh_loaded"
    all = "eh_all"
    version = "eh_version"


class ExerciseHistoryGetAllDTO(ExerciseHistoryGetAll):
    user_id: UUID


ListExerciseHistoryResponse = RootModel[list[ExerciseHistoryResponse]]
