from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from Backend.models.base import ModelT
from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout

from ..models.training_day_history import TrainingDayHistory

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class TrainingDayHistoryRepository(SQLAlchemyAbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=TrainingDayHistory)

    async def get_tr_day_history(
        self,
        id: int
    ) -> TrainingDayHistory | None:
        stmt = (
            select(TrainingDayHistory)
            .where(
                TrainingDayHistory.id == id,
            )
            .options(
                selectinload(TrainingDayHistory.exercises_history)
            )
        )

        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_tr_day_history(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        workout_id: int | None = None,
        day_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        ascending: bool = False
    ) -> Sequence[TrainingDayHistory]:
        stmt = (
            select(TrainingDayHistory)
            .join(TrainingDayHistory.training_day, isouter=True)
            .join(TrainingDay.workout)
            .where(Workout.user_id == user_id)
        )
        
        if workout_id:
            stmt = stmt.where(Workout.id == workout_id)
        
        if day_id:
            stmt = stmt.where(TrainingDay.id == day_id)

        if start_date:
            stmt = stmt.where(TrainingDayHistory.created_at >= start_date)

        if end_date:
            stmt = stmt.where(TrainingDayHistory.created_at <= end_date)

        if ascending:
            stmt = stmt.order_by(TrainingDayHistory.created_at.asc())
        else:
            stmt = stmt.order_by(TrainingDayHistory.created_at.desc())

        stmt = stmt.offset(skip).limit(limit)

        result = await self.execute(stmt)
        return result.scalars().all()
