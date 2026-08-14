from pydantic import BaseModel, Field

from typing import Annotated

from Backend.schemas.base import Str100, BaseResponse

from .day_exercise import DayExerciseResponse

DayOrderInt = Annotated[int, Field(gt=0, le=7)]

class TrainingDayBase(BaseModel):
    name: Str100
    day_order: DayOrderInt

class TrainingDayResponse(BaseResponse, TrainingDayBase):
    id: int

class TrainingDayRelataionsResponse(TrainingDayResponse):
    day_exercises: list[DayExerciseResponse] = []

class TrainingDayCreate(TrainingDayBase):
    pass

class TrainingDayCreateDTO(TrainingDayBase):
    workout_id: int

class TrainingDayUpdate(BaseModel):
    name: Str100 | None = None
    day_order: DayOrderInt | None = None


