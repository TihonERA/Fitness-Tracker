from sqlalchemy.ext.asyncio import AsyncSession 
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, bindparam, and_, CursorResult
from ..models.trainingday import TrainingDay
from ..models.dayexercise import  DayExercise
from typing import Type, Sequence, Any
from uuid import UUID

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workout_with_schedule(self, workout: Workout) -> Workout:
        self.add(workout)
        await self.commit()
        await self.refresh(workout)
        return workout

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
        user_id: UUID | None= None, 
        public: bool = False
    ) -> Sequence[int]:
        stmt = (
            select(Workout.workout_id)
            .where(Workout.public == public)
        )
        if user_id:
            stmt = stmt.where(Workout.user_id == user_id)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.execute(stmt)
        return result.scalars().all()
    
    async def update_day_exercise(self,
        day_exercises: list[dict[str, Any]]
    ) -> int:
          data = [
            {
                "p_day_id": ex["day_did"],
                "p_exercise_id": ex["exercise_id"],
                "p_order": ex["exercise_order"],
                "p_sets": ex["sets"],
                "p_reps": ex["reps"]
            }
            for ex in day_exercises if ex.get("exercise_id") and ex.get("day_id") 
          ]

          stmt = (
            update(DayExercise)
            .where(
                and_(
                    DayExercise.day_id == bindparam("p_day_id"),
                    DayExercise.exercise_id == bindparam("p_exercise_id")
                )
            )
            .values(
                exercise_order = bindparam("p_order"),
                sets = bindparam("p_sets"),
                reps = bindparam("p_reps")
            )
          )

          result = await self.db.execute(stmt, data) # type: ignore
          return result.rowcount # type: ignore

    
    def add(self, instance: object) -> None:
        self.db.add(instance)

    async def refresh(self, instance: object) -> None:
        await self.db.refresh(instance)

    async def commit(self) -> None:
        await self.db.commit()

    async def execute(self, stmt):
        return await self.db.execute(stmt)

   
