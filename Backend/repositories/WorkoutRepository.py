from sqlalchemy.ext.asyncio import AsyncSession 
from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository
from ..models.workout import Workout
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy import select 
from ..models.trainingday import TrainingDay
from ..models.dayexercise import  DayExercise
from ..models.muscle import Muscle
from ..models.exercise import Exercise
from ..models.muscle_antagonists import MuscleAntagonists
from typing import Sequence, Any
from uuid import UUID

class WorkoutRepository(SQLAlchemyAbstractRepository[Workout]):

    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(db, Workout)

    async def create_record_template(
        self,
        instance: Workout | TrainingDay 
    ) -> Workout:
        self.add(instance)

        await self.flush()
        
        workout_id: int = getattr(instance, "workout_id")
        stmt = self._get_loaded_workout_stmt(workout_id=workout_id)
        loaded_workout = await self.execute(stmt)
        
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
    
    async def update_workout(
        self,
        workout_id: int,
        data: dict[str, Any]     
    ) -> int: 
        return await self.update_by_column(
            column=Workout.workout_id,
            identificator=workout_id,
            data=data
        )

    async def delete_workout(self,
        workout_id: int
    ) -> int:
        return await self.delete_by_column(
            column=Workout.workout_id,
            identificator=workout_id
        )

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

    async def get_all_muscles_antagonists(
        self,
    ):
        muscles = aliased(Muscle, name="muscle")
        muscles_antagonists = aliased(Muscle, name="muscle_antagonist")
    
        stmt = (
            select(
                muscles.name.label("muscle"),
                muscles_antagonists.name.label("muscle_antagonist")
            )
            .select_from(MuscleAntagonists) 
            .join(muscles, muscles.muscle_id == MuscleAntagonists.muscle_id)
            .join(muscles_antagonists, muscles_antagonists.muscle_id == MuscleAntagonists.muscle_antagonist_id)
        )

        result = await self.execute(stmt)
        return result.tuples().all()
