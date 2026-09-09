from typing import Sequence, Tuple

from sqlalchemy import literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise
from Backend.models.exercise import Exercise
from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout
from Backend.repositories.SqlAlchemyAbstractRepository import (
    SQLAlchemyAbstractRepository,
)
from Backend.models.muscle import Muscle


class MuscleRepository(SQLAlchemyAbstractRepository[Muscle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Muscle)

    async def get_all_muscles(self) -> Sequence[str]:
        stmt = select(Muscle.name)

        result = await self.execute(stmt)
        return result.scalars().all()

    async def get_all_trained_muscles_from_workout(
        self, workout_id: int
    ) -> Sequence[dict]:
        stmt = (
            select(Exercise.muscle_activation)
            .join(Exercise.day_exercises)
            .join(DayExercise.training_day)
            .where(TrainingDay.workout_id == workout_id)
        )

        result = await self.execute(stmt)
        return result.scalars().all()
