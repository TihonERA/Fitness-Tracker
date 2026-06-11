from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ..models.trainingday import TrainingDay
from uuid import UUID

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workout_with_schedule(self, workout: Workout) -> Workout | None:
        self.add(workout)
        await self.commit()

        return await self.get_workout(workout.workout_id)

    async def get_workout(self, workout_id: int) -> Workout | None:
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
    
    async def get_all_workouts(self, 
        skip: int, 
        limit: int, 
        user_id: UUID|None=None, 
        public: bool = False
    ):
        stmt = (
            select(Workout)
            .where(Workout.public == public)
        )
        if user_id:
            stmt = stmt.where(Workout.user_id == user_id)

        stmt = stmt.offset(skip).limit(limit).options(
            selectinload(Workout.training_days)
            .selectinload(TrainingDay.day_exercises)
        )

        result = await self.execute(stmt)
        return result.scalars().all()
    
    def add(self, instance: object) -> None:
        self.db.add(instance)

    async def refresh(self, instance: object) -> None:
        await self.db.refresh(instance)

    async def commit(self) -> None:
        await self.db.commit()

    async def execute(self, stmt):
        return await self.db.execute(stmt)

    
