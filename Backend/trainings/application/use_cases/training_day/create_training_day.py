from typing import Protocol
from Backend.trainings.application.dto.training_day import CreateTrainingDayCommand
from Backend.trainings.application.ports.workout import WorkoutReaderPort
from Backend.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout


class TrainingDayCreator(Protocol):
    async def create(self, training_day: TrainingDay) -> TrainingDay: ...


class CreateTrainingDayUseCase:
    def __init__(
        self,
        workout_repo: WorkoutReaderPort,
        tr_day_repo: TrainingDayCreator,
    ) -> None:
        self.workout_repo = workout_repo
        self.tr_day_repo = tr_day_repo

    async def __call__(self, command: CreateTrainingDayCommand) -> TrainingDay:
        workout = await self.workout_repo.get(command.workout_id)

        if workout is None:
            raise WorkoutNotFound(command.workout_id)

        workout.ensure_ownership(command.user_id)

        training_day = TrainingDay.create(
            workout_id=command.workout_id,
            name=EntityTitle(command.name),
            day_order=DayOrder(command.day_order),
        )

        return await self.tr_day_repo.create(training_day)
