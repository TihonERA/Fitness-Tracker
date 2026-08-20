from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from Backend.models.base import ModelT
from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout
from Backend.schemas.training_day_history import TrainingDayHistoryGetAll

from ..models.training_day_history import TrainingDayHistory

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class TrainingDayHistoryRepository(SQLAlchemyAbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=TrainingDayHistory)

    async def get_tr_day_history(
        self,
        history_id: int
    ) -> TrainingDayHistory | None:
        return await self.get_instance_by_id(
            id=history_id,
            options=[selectinload(TrainingDayHistory.exercises_history)]
        )

    async def get_all_tr_day_history(
        self,
        data: TrainingDayHistoryGetAll
    ) -> Sequence[TrainingDayHistory]:
        stmt = (
            select(TrainingDayHistory)
            .join(TrainingDayHistory.training_day, isouter=True)
            .join(TrainingDay.workout)
            .where(Workout.user_id == data.user_id)
        )
        
        if data.workout_id:
            stmt = stmt.where(Workout.id == data.workout_id)
        
        if data.day_id:
            stmt = stmt.where(TrainingDay.id == data.day_id)

        if data.start_date:
            stmt = stmt.where(TrainingDayHistory.created_at >= data.start_date)

        if data.end_date:
            stmt = stmt.where(TrainingDayHistory.created_at <= data.end_date)

        if data.ascending:
            stmt = stmt.order_by(TrainingDayHistory.created_at.asc())
        else:
            stmt = stmt.order_by(TrainingDayHistory.created_at.desc())

        stmt = stmt.offset(data.skip).limit(data.limit)

        result = await self.execute(stmt)
        return result.scalars().all()
