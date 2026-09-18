from dataclasses import dataclass
from typing import Any
from uuid import UUID

from Backend.trainings.domain.exceptions.workout_exceptions import (
    DayExerciseNotFound,
    WorkoutAccessDenied,
)
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayNotFound,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.title import EntityTitle


@dataclass
class Workout:
    id: int | None
    user_id: UUID
    name: EntityTitle
    description: str | None
    public: bool
    training_days: list[TrainingDay]

    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: EntityTitle,
        description: str | None = None,
        public: bool = False,
    ) -> "Workout":
        return cls(
            id=None,
            user_id=user_id,
            name=name,
            description=description,
            public=public,
            training_days=[],
        )

    def ensure_ownership(self, user_id: UUID) -> None:
        if self.user_id != user_id:
            raise WorkoutAccessDenied()

    def update(
        self,
        name: EntityTitle | None = None,
        description: str | None = None,
        public: bool | None = None,
    ) -> None:
        if name:
            self.name = name

        if description is not None:
            self.description = description

        if public is not None:
            self.public = public

    def delete_day(self, day_id: int) -> None:
        old_days = self.training_days
        self.training_days = [d for d in old_days if d.id != day_id]
        if len(old_days) == len(self.training_days):
            raise TrainingDayNotFound(day_id)

    def delete_exercise(self, day_id: int, exercise_id: int) -> None:
        day = next((d for d in self.training_days if d.id == day_id), None)
        if day is None:
            raise TrainingDayNotFound(day_id)

        old_exercises = day.day_exercises
        day.day_exercises = [e for e in old_exercises if e.exercise_id != exercise_id]
        if len(old_exercises) == len(day.day_exercises):
            raise DayExerciseNotFound(day_id, exercise_id)
