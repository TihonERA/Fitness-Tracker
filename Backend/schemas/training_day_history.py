from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, RootModel

from Backend.schemas.exercise_history import ExerciseHistoryRelalationsResponse

from .base import BaseResponse, OptionalDateTime, OptionalInt, Str100, SkipInt, LimitInt


class TrainingDayHistoryBase(BaseModel):
    day_name: Str100


class TrainingDayHistoryCreate(TrainingDayHistoryBase):
    day_id: int


class TrainingDayHistoryResponse(BaseResponse, TrainingDayHistoryBase):
    id: int
    day_id: int
    created_at: datetime
    exercises_history: list[ExerciseHistoryRelalationsResponse] = []


class TrainingDayHistoryGetAll(BaseModel):
    skip: SkipInt
    limit: LimitInt
    workout_id: OptionalInt = None
    day_id: OptionalInt = None
    start_date: OptionalDateTime = None
    end_date: OptionalDateTime = None
    ascending: bool = False


class TrainingDayHistoryGetAllDTO(TrainingDayHistoryGetAll):
    user_id: UUID


class TrainingDayHistoryCachePrefixes(StrEnum):
    tag = "td_tag"
    get_loaded_key = "td_loaded"
    get_all_key = "td_all"
    version = "td_version"


ListTrDayHistoryResponse = RootModel[list[TrainingDayHistoryResponse]]
