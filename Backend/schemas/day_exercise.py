from pydantic import BaseModel, Field

from typing import Annotated

from Backend.schemas.base import BaseResponse

ExerciseOrderInt = Annotated[int, Field(gt=0, le=50)]
SetsInt = Annotated[int, Field(gt=0, le=30)]
RepsInt = Annotated[int, Field(gt=0, le=150)]

class DayExerciseBase(BaseModel):
    exercise_order: ExerciseOrderInt

class DayExerciseResponse(BaseResponse, DayExerciseBase):
    exercise_id: int

class DayExerciseCreate(DayExerciseBase):
    exercise_id: int

class DayExerciseCreateDTO(DayExerciseCreate):
    day_id: int
