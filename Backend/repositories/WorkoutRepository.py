from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ..models.trainingday import TrainingDay

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workout_with_schedule(self, workout: Workout) -> Workout:
        self.add(workout)
        await self.commit()

        return await self.get_workout(workout.workout_id)

    async def get_workout(self, workout_id: int):
        stmt = (
            select(Workout)
            .where(Workout.workout_id == workout_id)
            .options(
                selectinload(Workout.training_days)
                .selectinload(TrainingDay.day_exercises)
            )
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()
    
    def add(self, instance: object) -> None:
        self.db.add(instance)

    async def refresh(self, instance: object) -> None:
        await self.db.refresh(instance)

    async def commit(self) -> None:
        await self.db.commit()

    async def execute(self, stmt):
        return await self.db.execute(stmt)

    
