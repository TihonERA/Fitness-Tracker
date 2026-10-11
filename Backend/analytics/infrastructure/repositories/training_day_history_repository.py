from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.analytics.domain.training_day_history import TrainingDayHistory
from Backend.analytics.infrastructure.mappers.training_day_history_mapper import (
    TrainingDayHistoryMapper,
)
from Backend.analytics.infrastructure.models.training_day_history import (
    TrainingDayHistoryModel,
)


class TrainingDayHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, training_day_history: TrainingDayHistory
    ) -> TrainingDayHistory:
        try:
            training_day_history_model = TrainingDayHistoryMapper.to_orm(
                training_day_history
            )

            self.session.add(training_day_history_model)
            await self.session.flush()

            return TrainingDayHistoryMapper.to_domain(training_day_history_model)
        except IntegrityError as e:
            raise NotImplemented("assHOLE")

    async def delete(self, id: int) -> None:
        try:
            stmt = delete(TrainingDayHistoryModel).where(
                TrainingDayHistoryModel.id == id
            )

            await self.session.execute(stmt)
            await self.session.flush()
        except IntegrityError as e:
            raise NotImplemented("pe")
