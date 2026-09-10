from types import TracebackType
from typing import Any, Optional, Sequence, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from Backend.models.trainingday import TrainingDay
from Backend.infrastructure.MuscleRepository import MuscleRepository
from Backend.infrastructure.DayExerciseRepository import DayExerciseRepository
from Backend.infrastructure.ExerciseHistoryRepository import ExerciseHistoryRepository
from Backend.infrastructure.TrainingDayHistoryRepository import (
    TrainingDayHistoryRepository,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.infrastructure.TrainingDayRepository import TrainingDayRepository
from Backend.infrastructure.UserRepository import UserRepository
from Backend.infrastructure.WorkoutRepository import WorkoutRepository
from Backend.services.workout.interfaces import WorkoutUOWInterface


class UnitOfWork(BaseUOWInterface, WorkoutUOWInterface):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    @property
    def workout(self) -> WorkoutRepository:
        return WorkoutRepository(self.session)

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_maker()

        self.user = UserRepository(session=self.session)
        self.trainingday = TrainingDayRepository(session=self.session)
        self.trainingdayhistory = TrainingDayHistoryRepository(session=self.session)
        self.dayexercise = DayExerciseRepository(session=self.session)
        self.exercisehistory = ExerciseHistoryRepository(session=self.session)
        self.musclerepository = MuscleRepository(session=self.session)

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
