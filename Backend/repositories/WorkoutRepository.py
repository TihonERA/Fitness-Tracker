from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from ..models.trainingday import TrainingDay
from ..models.dayexercise import Exercise

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workout_with_schedule(self, workout: Workout):
        await self.db.add(workout)
        await self.db.commit()

        await self.db.refresh(
            workout,
            options=[
                selectinload(Workout.training_days)
                .selectinload(TrainingDay.day_exercises)
            ]
        )
        return workout
