from pydantic import BaseModel, Field
from .base import StrText, Str100, BaseResponse
from uuid import UUID
from typing import Annotated

DayOrderInt = Annotated[int, Field(gt=0, le=7)]

ExerciseOrderInt = Annotated[int, Field(gt=0, le=50)]
SetsInt = Annotated[int, Field(gt=0, le=30)]
RepsInt = Annotated[int, Field(gt=0, le=150)]

SkipInt = Annotated[int, Field(0, ge=0)]
LimitInt = Annotated[int, Field(20, gt=0, le=100)]

class DayExerciseBase(BaseModel):
    exercise_order: ExerciseOrderInt
    sets: SetsInt | None = None 
    reps: RepsInt | None = None

class TrainingDayBase(BaseModel):
    name: Str100 
    day_order: DayOrderInt

class WorkoutBase(BaseModel):
    name: Str100
    description: StrText | None = None

class DayExerciseResponse(BaseResponse, DayExerciseBase):
    exercise_id: int

class TrainingDayResponse(BaseResponse, TrainingDayBase):
    day_id: int

class TrainingDayRelataionsResponse(TrainingDayResponse):
    day_exercises: list[DayExerciseResponse] = []

class WorkoutResponse(BaseResponse, WorkoutBase):
    workout_id: int
    user_id: UUID
    public: bool
    rate: float

class WorkoutRelationsResponse(WorkoutResponse):
    training_days: list[TrainingDayRelataionsResponse] = []

class DayExerciseCreate(DayExerciseBase):
    exercise_id: int

class TrainingDayCreate(TrainingDayBase):
    day_exercises: list[DayExerciseCreate] = []

class WorkoutCreate(BaseResponse, WorkoutBase):
    user_id: UUID
    public: bool | None = None
    training_days: list[TrainingDayCreate] = []

class DayExerciseUpdate(BaseModel):
    exercise_order: ExerciseOrderInt | None = None
    sets: SetsInt | None = None
    reps: RepsInt | None = None

class TrainingDayUpdate(BaseModel):
    name: Str100 | None = None
    day_order: DayOrderInt | None = None

class WorkoutUpdate(BaseModel):
    name: Str100 | None = None
    description: StrText | None = None
    public: bool | None = None

class WorkoutGetAllFilter(BaseModel):
    skip: SkipInt
    limit: LimitInt
    public: bool
