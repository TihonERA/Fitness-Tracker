from dataclasses import dataclass

from Backend.trainings.domain.day_exercise_model import DayExercise


@dataclass
class TrainingDay:
    id: int
    workout_id: int
    name: str
    day_exercises: list[DayExercise]
