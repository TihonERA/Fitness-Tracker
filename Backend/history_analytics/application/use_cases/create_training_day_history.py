from typing import Protocol

from Backend.analytics.application.dto.training_day_history import (
    CreateTrainingDayHistoryCommand,
)
from Backend.analytics.domain.training_day_history import TrainingDayHistory
from Backend.shared.domain.value_objects.entity_title import EntityTitle


class TrainingDayHistoryCreater(Protocol):
    async def create(
        self, training_day_history: TrainingDayHistory
    ) -> TrainingDayHistory: ...


class CreateTrainingDayHistoryUseCase:
    def __init__(self, tr_day_history_repo: TrainingDayHistoryCreater) -> None:
        self.tr_day_history_repo = tr_day_history_repo

    async def __call__(
        self, command: CreateTrainingDayHistoryCommand
    ) -> TrainingDayHistory:
        training_day_history = TrainingDayHistory.create(
            day_id=command.day_id, day_name=EntityTitle(command.day_name)
        )

        return await self.tr_day_history_repo.create(training_day_history)
