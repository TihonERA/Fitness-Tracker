from sqlalchemy.ext.asyncio import AsyncSession

from Backend.schemas.workout import WorkoutGetAllFilterDTO 
from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository
from ..models.workout import Workout
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy import and_, select 
from ..models.trainingday import TrainingDay
from ..models.dayexercise import  DayExercise
from ..models.muscle import Muscle
from ..models.exercise import Exercise
from ..models.muscle_antagonists import MuscleAntagonists
from typing import Sequence, Any
from uuid import UUID

class WorkoutRepository(SQLAlchemyAbstractRepository[Workout]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Workout)

    async def get_workout(self, workout_id: int) -> Workout | None:
        stmt = (
            select(Workout)
            .where(Workout.id == workout_id)
            .options(
                selectinload(Workout.training_days)
                .selectinload(TrainingDay.day_exercises)
            )
        )

        result = await self.execute(stmt)
        return result.scalars().one_or_none()

    async def get_all_workouts(self, 
        data: WorkoutGetAllFilterDTO
    ) -> Sequence[Workout]:
        stmt = select(Workout)
        if data.target_user_id:
            stmt = stmt.where(
                Workout.user_id == data.target_user_id,
            )
        if data.public:
            stmt = stmt.where(
                Workout.public == data.public
            )
        stmt = stmt.offset(data.skip).limit(data.limit)

        result = await self.execute(stmt)
        return result.scalars().all()
    
    async def get_all_muscles(self):
        stmt = (
            select(Muscle.name)
        )

        result = await self.execute(stmt)
        return result.scalars().all()
        
    async def get_all_trainted_muscles_in_workout(self,
        id: int
    ):
        stmt = (
            select(Exercise.muscle_activation)
            .join(DayExercise)
            .join(TrainingDay)
            .where(TrainingDay.id == id)
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
            .join(muscles, muscles.id == MuscleAntagonists.muscle_id)
            .join(muscles_antagonists, muscles_antagonists.id == MuscleAntagonists.muscle_antagonist_id)
        )

        result = await self.execute(stmt)
        return result.tuples().all()
