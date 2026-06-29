from sqlalchemy.ext.asyncio import AsyncSession 
from ..models.workout import Workout
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select, update, bindparam, and_ 
from ..models.trainingday import TrainingDay
from ..models.dayexercise import  DayExercise
from ..models.base import Base
from ..models.muscle import Muscle
from ..models.exercise import Exercise
from typing import TypeVar, Sequence, Any
from uuid import UUID

ModelType = TypeVar("ModelType", bound=Base)

class WorkoutRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_instance(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def create_record_template(
        self,
        instance: Workout | TrainingDay 
    ) -> Workout:
        self.db.add(instance)

        await self.db.flush()
        
        workout_id: int = getattr(instance, "workout_id")
        stmt = self._get_loaded_workout_stmt(workout_id=workout_id)
        loaded_workout = await self.execute(stmt)
        
        await self.commit()
        return loaded_workout.scalar_one()

    async def get_workout(self, workout_id: int) -> Workout | None:
        stmt = self._get_loaded_workout_stmt(workout_id=workout_id)         
        result = await self.execute(stmt)
        return result.scalars().one_or_none()

    @staticmethod
    def _get_loaded_workout_stmt(workout_id: int):
        stmt = (
            select(Workout)
            .where(Workout.workout_id == workout_id)
            .options(
                selectinload(Workout.training_days)
                .selectinload(TrainingDay.day_exercises)
            )
            .execution_options(populate_existing=True)
        )
        return stmt
    
    async def get_all_workouts(self, 
        skip: int, 
        limit: int, 
        user_id: UUID | None = None, 
        public: bool = False
    ) -> Sequence[int]:
        stmt = select(Workout.workout_id)
        if user_id:
            stmt = stmt.where(
                Workout.user_id == user_id,
                Workout.public == public
            )
        else:
            stmt = stmt.where(Workout.public == True)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.execute(stmt)
        return result.scalars().all()
    
    async def update_day_exercise(self,
        day_exercises: list[dict[str, Any]]
    ) -> int:
          data = [
            {
                "p_training_day_id": ex["day_did"],
                "p_exercise_id": ex["exercise_id"],
                "p_order": ex["exercise_order"],
                "p_sets": ex["sets"],
                "p_reps": ex["reps"]
            }
            for ex in day_exercises if ex.get("exercise_id") and ex.get("training_day_id") 
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

    async def update_workout(self,
        workout_id: int,
        data: dict[str, Any]     
    ) -> int: 
        return await self._update_data(
            model=Workout,
            attribute="workout_id",
            id=workout_id,
            data=data
        )

    async def update_training_day(self,
        training_day_id: int,
        data: dict[str, Any]
    ) -> int:
        return await self._update_data(
            model=TrainingDay,
            attribute="training_day_id",
            id=training_day_id,
            data=data
        )

    async def _update_data(self,
        model: type[Base],
        attribute: str,
        id: int,
        data: dict[str, Any]
    ):
        stmt = (
            update(model)
            .where(getattr(model, attribute) == id)
            .values(**data)
        )

        result = await self.execute(stmt)
        return result.rowcount #type: ignore

    async def delete_workout(self,
        workout_id: int
    ) -> int:
        return await self._delete_data(
            model=Workout,
            attribute="workout_id",
            id=workout_id
        )

    async def delete_training_day(self,
        training_day_id: int
    ) -> int:
        return await self._delete_data(
            model=TrainingDay,
            attribute="training_day_id",
            id=training_day_id
        )

    async def _delete_data(self,
        model: type[Base],
        attribute: str,
        id: int
    ):
        stmt = (
            delete(model)
            .where(getattr(model, attribute) == id)
        )

        result = await self.execute(stmt)
        return result.rowcount # type: ignore

    async def delete_day_exercise(self,
        training_day_id: int,
        exercise_id: int
    ) -> int:
        stmt = (
            delete(DayExercise)
            .where(
                and_(
                    DayExercise.day_id == training_day_id,
                    DayExercise.exercise_id == exercise_id 
                )
            )
        ) 

        result = await self.execute(stmt)
        return result.rowcount # type: ignore

    async def get_all_muscles(self):
        stmt = (
            select(Muscle.name)
        )

        result = await self.execute(stmt)
        return result.scalars().all()
        
    async def get_all_trainted_muscles_in_workout(self,
        workout_id: int
    ):
        stmt = (
            select(Exercise.muscle_activation)
            .join(DayExercise)
            .join(TrainingDay)
            .where(TrainingDay.workout_id == workout_id)
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

     
