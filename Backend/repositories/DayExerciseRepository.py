from typing import Any

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class DayExerciseRepository(SQLAlchemyAbstractRepository[DayExercise]):

    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session, DayExercise)

    async def update_day_exercise(
        self,
        day_id,
        exercise_id,
        data: dict[str, Any]
    ) -> int:
        stmt = (
            update(self.model)
            .where(
                self.model.day_id == day_id,
                self.model.exercise_id == exercise_id
            )
            .values(**data)
        )

        result = await self.execute(stmt)
        return result.rowcount #type: ignore

    async def delete_day_exercise(
        self,
        day_id: int,
        exercise_id: int
    ) -> int:
        stmt = (
            delete(self.model)
            .where(
                self.model.day_id == day_id,
                self.model.exercise_id == exercise_id
            )
        )

        result = await self.execute(stmt)
        return result.rowcount #type: ignore
