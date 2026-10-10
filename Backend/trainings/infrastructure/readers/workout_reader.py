from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.trainings.application.dto.training_day import (
    TrainingDayDetailDTO,
)
from Backend.trainings.application.dto.workout import WorkoutDetailDTO, WorkoutReadDTO
from Backend.trainings.infrastructure.mappers.workout_mapper import WorkoutMapper
from Backend.trainings.infrastructure.models.workout import WorkoutModel


class WorkoutReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_loaded(self, id: int) -> WorkoutDetailDTO | None:
        workout = await self.session.get(
            WorkoutModel, id, options=[selectinload(WorkoutModel.training_days)]
        )

        if workout is None:
            return None

        return WorkoutMapper.to_dto_loaded(workout)

    async def get_unloaded(self, id: int) -> WorkoutReadDTO | None:
        workout = await self.session.get(WorkoutModel, id)

        if workout is None:
            return None

        return WorkoutMapper.to_dto_unloaded(workout)
