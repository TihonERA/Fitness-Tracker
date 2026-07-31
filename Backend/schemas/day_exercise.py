from pydantic import BaseModel, Field

from typing import Annotated

from Backend.schemas.base import BaseResponse

ExerciseOrderInt = Annotated[int, Field(gt=0, le=50)]
SetsInt = Annotated[int, Field(gt=0, le=30)]
RepsInt = Annotated[int, Field(gt=0, le=150)]

class DayExerciseBase(BaseModel):
    exercise_order: ExerciseOrderInt
    sets: SetsInt | None = None 
    reps: RepsInt | None = None

class DayExerciseResponse(BaseResponse, DayExerciseBase):
    exercise_id: int

class DayExerciseCreate(DayExerciseBase):
    exercise_id: int

class DayExerciseUpdate(BaseModel):
    exercise_order: ExerciseOrderInt | None = None
    sets: SetsInt | None = None
    reps: RepsInt | None = None
