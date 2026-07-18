from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, Sequence, Any

from sqlalchemy.orm import InstrumentedAttribute
from ..models.base import ModelT

class SQLAlchemyAbstractRepository(Generic[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]):
        self.session = session
        self.model = model

    async def create_instance(self, instance):
        self.add(instance)
        await self.flush()
        await self.refresh(instance)
        return instance
    
    async def update_by_column(
        self,
        column: InstrumentedAttribute,
        identificator: int | UUID,
        data: dict[str, Any],
    ):
        stmt = (
            update(self.model)
            .where(column == identificator)
            .values(**data)
            .returning(self.model)
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_by_column(
        self,
        column: InstrumentedAttribute,
        identificator: int | UUID
    ) -> int:
        stmt = (
            delete(self.model)
            .where(column == identificator)
        )
        result = await self.execute(stmt)
        return result.rowcount #type: ignore

    def add(self, instance: object, **kwargs) -> None:
        self.session.add(instance, **kwargs)

    async def refresh(self, instance: object, **kwargs) -> None:
        await self.session.refresh(instance, **kwargs)

    async def execute(self, stmt, **kwargs):
        return await self.session.execute(stmt, **kwargs)

    async def flush(self, instance: Sequence[Any] | None = None) -> None:
        await self.session.flush(instance)

