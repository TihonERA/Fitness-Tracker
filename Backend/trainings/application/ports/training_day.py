from typing import Protocol
from uuid import UUID

from Backend.trainings.domain.training_day_model import TrainingDay


class TrainingDayRepositoryPort(Protocol):
    async def get(self, id: int) -> TrainingDay: ...
    async def save(self, training_day: TrainingDay) -> TrainingDay: ...


class TrainingDayAccessServicePort(Protocol):
    async def get_authorized_day(
        self, user_id: UUID, workout_id: int, day_id: int
    ) -> TrainingDay: ...
