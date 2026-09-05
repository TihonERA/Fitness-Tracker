from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.models import training_day_history
from Backend.models.sets_history import SetsHistory
from Backend.models.exercise import Exercise
from Backend.repositories.SqlAlchemyAbstractRepository import (
    SQLAlchemyAbstractRepository,
)

from Backend.models.exercise_history import ExerciseHistory
from Backend.schemas.exercise_history import (
    ExerciseHistoryCreateDTO,
    ExerciseHistoryGetAllDTO,
    SetsHistoryCreate,
)
from Backend.utils.exceptions import DBErrorHandler


class ExerciseHistoryRepository(SQLAlchemyAbstractRepository[ExerciseHistory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ExerciseHistory)

    def _make_sets_history(self, data: list[SetsHistoryCreate]) -> list[SetsHistory]:
        sets_history = [SetsHistory(**s.model_dump(exclude_unset=True)) for s in data]
        return sets_history

    def _make_exercise_history(self, data: ExerciseHistoryCreateDTO) -> ExerciseHistory:
        sets_history = self._make_sets_history(data.sets_history)

        ex_history = ExerciseHistory(
            user_id=data.user_id,
            exercise_id=data.exercise_id,
            training_day_history_id=data.training_day_history_id,
            sets_history=sets_history,
        )

        return ex_history

    async def create_bulk_exercise_history(
        self, data: list[ExerciseHistoryCreateDTO]
    ) -> list[ExerciseHistory]:
        histories = [self._make_exercise_history(ex_data) for ex_data in data]

        try:
            self.session.add_all(histories)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)

        return histories

    async def get_exercise_history(self, history_id: int) -> ExerciseHistory | None:
        return await self.get_instance_by_id(
            id=history_id, options=[selectinload(ExerciseHistory.sets_history)]
        )

    async def get_all_histories(
        self, data: ExerciseHistoryGetAllDTO
    ) -> Sequence[ExerciseHistory]:
        stmt = select(ExerciseHistory).where(
            ExerciseHistory.user_id == data.user_id,
            ExerciseHistory.exercise_id == data.exercise_id,
        )
        if data.start_date:
            stmt = stmt.where(ExerciseHistory.created_at >= data.start_date)
        if data.end_date:
            stmt = stmt.where(ExerciseHistory.created_at <= data.end_date)

        stmt = stmt.offset(data.skip).limit(data.limit)

        result = await self.execute(stmt)
        return result.scalars().all()
