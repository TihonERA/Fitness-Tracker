from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ..models.trainingday import TrainingDay
from ..models.dayexercise import Exercise

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workout_with_schedule(self, workout: Workout) -> Workout:
        self.add(workout)
        await self.db.commit()

        stmt = (
            select(Workout)
            .where(Workout.workout_id == workout.workout_id)
            .options(
                selectinload(Workout.training_days)
                .selectinload(TrainingDay.day_exercises)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    def add(self, instance: object) -> None:
        self.db.add(instance)

    async def refresh(self, instance: object) -> None:
        await self.db.refresh(instance)

    async def commit(self) -> None:
        await self.db.commit()

    
