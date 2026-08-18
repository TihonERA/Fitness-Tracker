from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse, OptionalDateTime, OptionalInt, Str100, SkipInt, LimitInt

class TrainingDayHistoryBase(BaseModel):
    day_name: Str100

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
