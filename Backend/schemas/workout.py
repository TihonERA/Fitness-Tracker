from pydantic import BaseModel, Field
from .base import StrText, Str100, BaseResponse

from .training_day import TrainingDayRelataionsResponse

from uuid import UUID
from typing import Annotated

SkipInt = Annotated[int, Field(0, ge=0)]
LimitInt = Annotated[int, Field(20, gt=0, le=100)]

class WorkoutBase(BaseModel):
    name: Str100
    description: StrText | None = None

class WorkoutResponse(BaseResponse, WorkoutBase):
    workout_id: int
    user_id: UUID
    public: bool
    rate: float

class WorkoutRelationsResponse(WorkoutResponse):
    training_days: list[TrainingDayRelataionsResponse] = []

class WorkoutCreate(WorkoutBase):
    public: bool = False

class WorkoutUpdate(BaseModel):
    name: Str100 | None = None
    description: StrText | None = None
    public: bool | None = None

class WorkoutGetAllFilter(BaseModel):
    skip: SkipInt
    limit: LimitInt
    user_id: UUID | None = None
    public: bool | None = None
