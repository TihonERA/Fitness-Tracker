from typing import Any
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise
from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class DayExerciseRepository(SQLAlchemyAbstractRepository[DayExercise]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, DayExercise)

    async def get_day_exercise(
        self,
        day_id: int,
        exercise_id: int
    ) -> DayExercise | None:
        stmt = (
            select(DayExercise)
            .where(
                DayExercise.day_id == day_id,
                DayExercise.exercise_id == exercise_id
            )
        )

        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def get_day_exercise_for_update( 
        self,
        day_id: int,
        exercise_id: int
    ) -> DayExercise | None:
        stmt = (
            select(DayExercise)
            .where(
                DayExercise.day_id == day_id,
                DayExercise.exercise_id == exercise_id
            )
            .with_for_update()
        )

        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_day_exercise(
        self,
        day_id: int,
        exercise_id: int
    ) -> None:
        stmt = (
            delete(self.model)
            .where(
                self.model.day_id == day_id,
                self.model.exercise_id == exercise_id
            )
        )

        result = await self.execute(stmt)
