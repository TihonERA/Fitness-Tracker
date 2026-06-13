from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class DayExercisesScheme(BaseModel):
    exercise_id: int
    exercise_order: int = Field(gt=0, le=50,)
    sets: int | None = Field(None, gt=0, le=30, description="Количество подходов")
    reps: int | None = Field(None, gt=0, le=150, description="Количество повторений")

class TrainingDayScheme(BaseModel):
    name: str = Field(max_length=100)
    day_order: int = Field(gt=0, le=7)
    day_exercises: list[DayExercisesScheme] | None = Field(None)

class WorkoutScheme(BaseModel):
    user_id: UUID 
    name: str  = Field(max_length=100)
    description: str | None = Field(default=None, max_length=2000) 
    training_days: list[TrainingDayScheme] | None = Field(None)

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class DayExerciseResponse(BaseResponse):
    exercise_id: int
    exercise_order: int
    sets: int | None
    reps: int | None

class TrainingDayResponse(BaseResponse):
    day_id: int               
    name: str
    day_order: int
    day_exercises: list[DayExerciseResponse]

class WorkoutResponse(BaseResponse):
    workout_id: int           
    user_id: UUID
    name: str
    description: str | None
    rate: float
    training_days: list[TrainingDayResponse]

class WorkoutsFilter(BaseResponse):
    skip: int = Field(0, ge=0)
    limit: int = Field(50, gt=0, le=500)
    public: bool = Field(default=False)

class UpdateDayExercise(DayExercisesScheme):
    day_id: int

class UpdateWorkout(WorkoutScheme):
    user_id: UUID = Field(exclude=True)
    training_days: list[TrainingDayScheme] | None = Field(exclude=True)

class UpdateTrainingDays(TrainingDayScheme):
    day_exercises: list[DayExercisesScheme] | None = Field(exclude=True)
 


