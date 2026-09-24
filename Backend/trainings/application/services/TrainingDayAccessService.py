from typing import Protocol
from uuid import UUID

from Backend.trainings.application.ports.workout import WorkoutReaderPort
from Backend.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayNotFound,
)
from Backend.trainings.domain.training_day_model import TrainingDay


class TrainingDayReader(Protocol):
    async def get(self, id: int) -> TrainingDay | None: ...


class TrainingDayAccessService:
    def __init__(
        self, workout_repo: WorkoutReaderPort, tr_day_repo: TrainingDayReader
    ) -> None:
        self.workout_repo = workout_repo
        self.tr_day_repo = tr_day_repo

    async def get_authorized_day(
        self, user_id: UUID, workout_id: int, day_id: int
    ) -> TrainingDay:
        workout = await self.workout_repo.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)
        workout.ensure_ownership(user_id)

        training_day = await self.tr_day_repo.get(day_id)

        if training_day is None:
            raise TrainingDayNotFound(day_id)
        training_day.ensure_ownership(workout_id)

        return training_day
