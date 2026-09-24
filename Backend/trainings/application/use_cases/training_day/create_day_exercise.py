from typing import Protocol

from Backend.trainings.application.dto.training_day import CreateDayExerciseCommand
from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
    TrainingDayRepositoryPort,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.exercise_order import ExerciseOrder


class CreateDayExerciseUseCase:
    def __init__(
        self,
        access_service: TrainingDayAccessServicePort,
        tr_day_repo: TrainingDayRepositoryPort,
    ) -> None:
        self.access_service = access_service
        self.tr_day_repo = tr_day_repo

    async def __call__(self, command: CreateDayExerciseCommand) -> TrainingDay:
        training_day = await self.access_service.get_authorized_day(
            command.user_id, command.workout_id, command.day_id
        )

        training_day.add_exercise(command.exercise_id, command.exercise_order)

        return await self.tr_day_repo.save(training_day)
