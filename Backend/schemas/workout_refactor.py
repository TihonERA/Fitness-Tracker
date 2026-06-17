from pydantic import BaseModel, Field, ConfigDict
from .base import DescriptionStr, NameStr, BaseResponse
from uuid import UUID
from typing import Annotated

DayOrderInt = Annotated[int, Field(gt=0, le=7)]

ExerciseOrderInt = Annotated[int, Field(gt=0, le=50)]
SetsInt = Annotated[int, Field(gt=0, le=30)]
RepsInt = Annotated[int, Field(gt=0, le=150)]


class WorkoutBase(BaseModel):
    name: NameStr
    description: DescriptionStr | None = None

class TrainingDayBase(BaseModel):
    name: NameStr 
    day_order: DayOrderInt

class DayExerciseBase(BaseModel):
    exercise_order: ExerciseOrderInt
    sets: SetsInt | None = None 
    reps: RepsInt | None = None

class WorkoutResponse(BaseResponse, WorkoutBase):
    workout_id: int
    user_id: UUID
    public: bool
    rate: float
    training_days: list[TrainingDayResponse] | None = None

class TrainingDayResponse(BaseResponse, TrainingDayBase):
    day_id: int
    day_exercises: list[DayExerciseResponse] | None = None

class DayExerciseResponse(BaseResponse, DayExerciseBase):
    exercise_id: int

class WorkoutCreate(BaseResponse, WorkoutBase):
    user_id: UUID
    public: bool | None = None
    training_days: list[TrainingDayCreate] | None = Field(default=None)

class TrainingDayCreate(BaseResponse, TrainingDayBase):
    workout_id: int
    day_exercises: list[DayExerciseCreate] | None = Field(default=None)

class DayExerciseCreate(BaseResponse, DayExerciseBase):
    day_id: int
    exercise_id: int

class WorkoutUpdate(BaseModel):
    name: NameStr | None = None
    description: DescriptionStr | None = None
    public: bool | None = None 

class TrainingDayUpdate(BaseModel):
    name: NameStr | None = None
    day_order: DayOrderInt | None = None

class DayExerciseUpdate(BaseModel):
    exercise_order: ExerciseOrderInt | None = None
    sets: SetsInt | None = None
    reps: RepsInt | None = None
