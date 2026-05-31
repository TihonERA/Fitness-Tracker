from pydantic import BaseModel, Field
from uuid import UUID

class DayExercisesScheme(BaseModel):
    exercises_id: int
    exercise_order: int = Field(gt=0, le=50,)
    sets: int | None = Field(None, gt=0, le=30, description="Количество подходов")
    reps: int | None = Field(None, gt=0, le=150, description="Количество повторений")

class TrainingDayScheme(BaseModel):
    day_id: int
    workout_id: int
    name: str = Field(max_length=100)
    day_order: int = Field(gt=0, le=7)
    day_exercises: list[DayExercisesScheme] | None = Field(None)

class WorkoutScheme(BaseModel):
    user_id: UUID 
    name: str  = Field(max_length=100)
    description: str | None = Field(default=None, max_length=2000) 
    rate: float = Field(default=0.0, ge=0.0, le=10.0)
    training_days: list[TrainingDayScheme] | None = Field(None)