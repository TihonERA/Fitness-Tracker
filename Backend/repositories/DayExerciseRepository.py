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
        self.session = session
        super().__init__(session, DayExercise)

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

    async def get_day_exercise_and_check_access(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ) -> DayExercise | None:
        stmt = (
            select(DayExercise)
            .join(TrainingDay, TrainingDay.day_id == DayExercise.day_id)
            .join(Workout, Workout.workout_id == TrainingDay.workout_id)
            .where(
                Workout.user_id == user_id,
                TrainingDay.workout_id == workout_id,
                DayExercise.day_id == day_id,
                DayExercise.exercise_id == exercise_id
            )
        )

        result = await self.execute(stmt)
        return result.scalar_one_or_none()

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
