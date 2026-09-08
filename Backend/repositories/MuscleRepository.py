from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.repositories.SqlAlchemyAbstractRepository import (
    SQLAlchemyAbstractRepository,
)
from Backend.models.muscle import Muscle


class MuscleRepository(SQLAlchemyAbstractRepository[Muscle]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Muscle)

    async def get_all(self) -> Sequence[Muscle]:
        stmt = select(Muscle)

        result = await self.execute(stmt)
        return result.scalars().all()
