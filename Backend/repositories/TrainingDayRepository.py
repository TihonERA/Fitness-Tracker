from typing import Any
from uuid import UUID

from sqlalchemy import join, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload

from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class TrainingDayRepository(SQLAlchemyAbstractRepository[TrainingDay]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TrainingDay)

    async def get_loaded_training_day(
        self,
        day_id: int
    ) -> TrainingDay | None:
        stmt = (
            select(self.model)
            .where(self.model.id == day_id)
            .options(
                selectinload(self.model.day_exercises)
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
