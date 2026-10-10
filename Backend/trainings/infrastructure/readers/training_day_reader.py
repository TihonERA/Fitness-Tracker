from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.trainings.application.dto.training_day import TrainingDayDetailDTO
from Backend.trainings.infrastructure.mappers.training_day_mapper import (
    TrainingDayMapper,
)
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel


class TrainingDayReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_loaded(self, id: int) -> TrainingDayDetailDTO | None:
        training_day = await self.session.get(
            TrainingDayModel,
            id,
            options=[selectinload(TrainingDayModel.day_exercises)],
        )

        if training_day is None:
            return None

        return TrainingDayMapper.to_dto(training_day)
