from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.trainingday import TrainingDay

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class TrainingDayRepository(SQLAlchemyAbstractRepository[TrainingDay]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session, TrainingDay)

    async def update_training_day(
        self,
        day_id: int,
        data: dict[str, Any]
    ):
        return await self.update_by_column(
            column=self.model.day_id,
            identificator=day_id,
            data=data
        )

    async def delete_training_day(
        self,
        day_id: int
    ) -> int:
        return await self.delete_by_column(
            column=self.model.day_id,
            identificator=day_id
        )
