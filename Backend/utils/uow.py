from types import TracebackType 
from typing import Any, Optional, Sequence, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from Backend.models.trainingday import TrainingDay
from Backend.repositories.DayExerciseRepository import DayExerciseRepository
from Backend.repositories.TrainingDayRepository import TrainingDayRepository
from Backend.repositories.UserRepository import UserRepository
from Backend.repositories.WorkoutRepository import WorkoutRepository

class UnitOfWork:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def __aenter__(self) -> "UnitOfWork": 
        self.session = self.session_maker()

        self.user = UserRepository(session=self.session)
        self.workout = WorkoutRepository(session=self.session)
        self.trainingday = TrainingDayRepository(session=self.session)
        self.dayexercise = DayExerciseRepository(session=self.session)

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
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
