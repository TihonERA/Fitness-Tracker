from typing import Protocol
from uuid import UUID

from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
)
from Backend.trainings.domain.training_day_model import TrainingDay


class GetDayExerciseUseCase:
    def __init__(self, access_service: TrainingDayAccessServicePort) -> None:
        self.access_service = access_service

    async def __call__(
        self, user_id: UUID, workout_id: int, day_id: int
    ) -> TrainingDay:
        return await self.access_service.get_authorized_day(user_id, workout_id, day_id)
