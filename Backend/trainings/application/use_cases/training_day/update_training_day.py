from typing import Protocol

from Backend.trainings.application.dto.training_day import UpdateTrainingDayCommand
from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
    TrainingDayRepositoryPort,
)
from Backend.trainings.application.ports.workout import WorkoutReaderPort
from Backend.trainings.domain import training_day_model
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.shared.domain.value_objects.entity_title import EntityTitle


class UpdateTrainingDay:
    def __init__(
        self,
        access_service: TrainingDayAccessServicePort,
        tr_day_repo: TrainingDayRepositoryPort,
    ) -> None:
        self.access_service = access_service
        self.tr_day_repo = tr_day_repo

    async def __call__(self, command: UpdateTrainingDayCommand) -> TrainingDay:
        training_day = await self.access_service.get_authorized_day(
            command.user_id, command.workout_id, command.day_id
        )

        training_day.update(
            EntityTitle(command.name) if command.name else None,
            DayOrder(command.day_order) if command.day_order else None,
        )

        return await self.tr_day_repo.save(training_day)
