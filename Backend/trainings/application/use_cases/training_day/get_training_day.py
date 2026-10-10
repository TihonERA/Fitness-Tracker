from typing import Protocol
from uuid import UUID

from Backend.tests.unit.trainings.training_day.conftest import tr_day_repo
from Backend.trainings.application.dto.training_day import TrainingDayDetailDTO
from Backend.trainings.application.dto.workout import WorkoutReadDTO
from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
)
from Backend.trainings.application.ports.workout import WorkoutReaderPort
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
    TrainingDayNotFound,
)
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)
from Backend.trainings.domain.training_day_model import TrainingDay


class TrainingDayReaderPort(Protocol):
    async def get_loaded(self, id: int) -> TrainingDayDetailDTO | None: ...


class WorkoutUnloadedReaderPort(Protocol):
    async def get_unloaded(self, id: int) -> WorkoutReadDTO | None: ...


class GetTrainingDayUseCase:
    def __init__(
        self,
        workout_reader: WorkoutUnloadedReaderPort,
        tr_day_reader: TrainingDayReaderPort,
    ) -> None:
        self.workout_reader = workout_reader
        self.tr_day_reader = tr_day_reader

    async def __call__(
        self, user_id: UUID, workout_id: int, day_id: int
    ) -> TrainingDayDetailDTO:
        workout = await self.workout_reader.get_unloaded(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if not workout.public and workout.user_id != user_id:
            raise WorkoutAccessDenied()

        training_day = await self.tr_day_reader.get_loaded(day_id)

        if training_day is None:
            raise TrainingDayNotFound

        if training_day.workout_id != workout_id:
            raise TrainingDayAccessDenied()

        return training_day
