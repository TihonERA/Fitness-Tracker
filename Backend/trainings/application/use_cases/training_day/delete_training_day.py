from typing import Protocol
from uuid import UUID

from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
    TrainingDayRepositoryPort,
)
from Backend.trainings.application.ports.workout import WorkoutReaderPort
from Backend.trainings.domain import training_day_model
from Backend.trainings.domain.training_day_model import TrainingDay


class TrainingDayDeleter(Protocol):
    async def delete(self, id: int) -> None: ...


class DeleteTrainingDayUseCase:
    def __init__(
        self,
        access_service: TrainingDayAccessServicePort,
        tr_day_repo: TrainingDayDeleter,
    ) -> None:
        self.access_service = access_service
        self.tr_day_repo = tr_day_repo

    async def __call__(self, user_id: UUID, workout_id: int, day_id: int) -> None:
        training_day = await self.access_service.get_authorized_day(
            user_id, workout_id, day_id
        )

        await self.tr_day_repo.delete(day_id)
