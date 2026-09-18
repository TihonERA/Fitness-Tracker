from dataclasses import dataclass

from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.workout_exceptions import (
    NameException,
    TrainingDayOrderException,
)
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class TrainingDay:
    id: int | None
    workout_id: int
    name: EntityTitle
    day_order: DayOrder
    day_exercises: list[DayExercise]

    @classmethod
    def create(
        cls, workout_id: int, name: EntityTitle, day_order: DayOrder
    ) -> "TrainingDay":
        return cls(
            id=None,
            workout_id=workout_id,
            name=name,
            day_order=day_order,
            day_exercises=[],
        )

    def update(
        self, name: EntityTitle | None = None, day_order: DayOrder | None = None
    ) -> None:
        if name:
            self.name = name

        if day_order:
            self.day_order = day_order
