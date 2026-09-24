from dataclasses import dataclass
from uuid import UUID

from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.exercise_order import ExerciseOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass(frozen=True)
class CreateTrainingDayCommand:
    user_id: UUID
    workout_id: int
    name: str
    day_order: int


@dataclass(frozen=True)
class UpdateTrainingDayCommand:
    user_id: UUID
    workout_id: int
    day_id: int
    name: str | None = None
    day_order: int | None = None


@dataclass(frozen=True)
class GetTrainingDayCommand:
    user_id: UUID


@dataclass(frozen=True)
class BaseDayExerciseCommand:
    user_id: UUID
    workout_id: int
    day_id: int
    exercise_id: int
    exercise_order: int


@dataclass(frozen=True)
class CreateDayExerciseCommand(BaseDayExerciseCommand): ...


@dataclass(frozen=True)
class UpdateDayExerciseCommand(BaseDayExerciseCommand): ...


@dataclass(frozen=True)
class TrainingDayReadDTO:
    id: int
    workout_id: int
    name: str
    day_order: int
