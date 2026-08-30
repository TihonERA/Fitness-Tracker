from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse, OptionalDateTime, OptionalInt, Str100, SkipInt, LimitInt

class TrainingDayHistoryBase(BaseModel):
    day_name: Str100

class TrainingDayHistoryCreate(TrainingDayHistoryBase):
    day_id: int

class TrainingDayHistoryResponse(BaseResponse, TrainingDayHistoryBase):
    id: int
    day_id: int
    created_at: datetime

class TrainingDayHistoryGetAll(BaseModel):
    user_id: UUID 
    skip: SkipInt
    limit: LimitInt
    workout_id: OptionalInt = None
    day_id: OptionalInt = None
    start_date: OptionalDateTime = None
    end_date: OptionalDateTime = None
    ascending: bool = False

class TrainingDayCachePrefixes(StrEnum):
    tag = "td_tag"
    get_loaded_key = "td_loaded"
    get_all_key = "td_all"
    version = "td_version"
