from sqlalchemy.ext.asyncio import AsyncSession

from Backend.schemas.workout import WorkoutGetAllFilterDTO
from Backend.services.workout.interfaces import WorkoutRepositoryInterface
from Backend.infrastructure.base_repository_components.base_read_repository import (
    BaseReadRepository,
)
from Backend.models.workout import Workout
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy import and_, select
from Backend.models.trainingday import TrainingDay
from Backend.models.dayexercise import DayExercise
from Backend.models.muscle import Muscle
from Backend.models.exercise import Exercise
from Backend.models.muscle_antagonists import MuscleAntagonists
from typing import Sequence, Any
from uuid import UUID


class WorkoutRepository(WorkoutRepositoryInterface, BaseReadRepository[Workout]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Workout)

    async def get_loaded(self, id: int) -> Workout | None:
        return await self.get_instance_by_column(
            column=Workout.id,
            search_value=id,
            options=[
                selectinload(Workout.training_days).selectinload(
                    TrainingDay.day_exercises
                )
            ],
        )

    async def get_all(self, data: WorkoutGetAllFilterDTO) -> Sequence[Workout]:
        stmt = select(Workout)
        if data.target_user_id:
            stmt = stmt.where(
                Workout.user_id == data.target_user_id,
            )
        if data.public:
            stmt = stmt.where(Workout.public == data.public)
        stmt = stmt.offset(data.skip).limit(data.limit)

        result = await self.execute(stmt)
        return result.scalars().all()
