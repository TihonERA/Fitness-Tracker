from pydantic import BaseModel, Field, RootModel

from Backend.utils.exceptions import Forbidden
from .base import StrText, Str100, BaseResponse

from .training_day import TrainingDayRelataionsResponse

from enum import StrEnum

from pydantic import model_validator

from uuid import UUID
from typing import Annotated

SkipInt = Annotated[int, Field(0, ge=0)]
LimitInt = Annotated[int, Field(20, gt=0, le=100)]

class WorkoutBase(BaseModel):
    name: Str100
    description: StrText | None = None

class WorkoutResponse(BaseResponse, WorkoutBase):
    id: int
    user_id: UUID
    public: bool

class WorkoutRelationsResponse(WorkoutResponse):
    training_days: list[TrainingDayRelataionsResponse] = []

class WorkoutCreate(WorkoutBase):
    public: bool = False

class WorkoutCreateDTO(WorkoutCreate):
    user_id: UUID

class WorkoutUpdate(BaseModel):
    name: Str100 | None = None
    description: StrText | None = None
    public: bool | None = None

class WorkoutGetAllFilter(BaseModel):
    skip: SkipInt
    limit: LimitInt
    user_id: UUID | None = None
    public: bool | None = None

class WorkoutGetAllFilterDTO(BaseModel):
    skip: int
    limit: int
    owner_id: UUID = Field(exclude=True)
    target_user_id: UUID | None
    public: bool | None

    @model_validator(mode="after")
    def validate_access(self) -> "WorkoutGetAllFilterDTO":
        if self.target_user_id is None:
            self.target_user_id = self.owner_id
            return self

        if self.public is False and self.target_user_id is not None and self.owner_id != self.target_user_id:
            raise Forbidden("You cant see private trainings of other user")

        return self

class WorkoutCachePrefixes(StrEnum):
    all_workouts = "workouts:all"
    loaded_workout = "loaded_workout"
    version = "workouts:version"

ListWorkoutResponse = RootModel[list[WorkoutResponse]]
