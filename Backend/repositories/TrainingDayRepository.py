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
        self.session = session
        super().__init__(session, TrainingDay)

    async def get_training_day(
        self,
        day_id: int
    ) -> TrainingDay | None:
        stmt = (
            select(self.model)
            .where(self.model.day_id == day_id)
            .options(
                selectinload(self.model.day_exercises)
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_training_day_for_update(
        self,
        day_id: int
    ) -> TrainingDay | None:
        return await self.get_instance_for_update(
            column=TrainingDay.day_id,
            identificator=day_id
        )

    async def get_training_day_and_check_access(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
    ) -> TrainingDay | None:
        stmt = (
            select(TrainingDay)
            .join(Workout, TrainingDay.workout_id == Workout.workout_id)
            .where(
                Workout.user_id == user_id,
                Workout.workout_id == workout_id,
                TrainingDay.day_id == day_id
            )
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_training_day(
        self,
        day_id: int
    ) -> int:
        return await self.delete_by_column(
            column=self.model.day_id,
            identificator=day_id
        )
