from uuid import UUID

from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, Sequence, Any

from sqlalchemy.orm import InstrumentedAttribute
from ..models.base import ModelT

class SQLAlchemyAbstractRepository(Generic[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]):
        self.session = session
        self.model = model

    async def add_and_refresh_instance(self, instance) -> ModelT:
        self.add(instance)
        await self.flush()
        await self.refresh(instance)
        return instance

    async def create_instance(self, data: dict[str, Any]) -> ModelT:
        filtered_data = {k: v for k, v in data.items() if k in self.model.__table__.columns.keys()}
        instance = self.model(**filtered_data)
        return await self.add_and_refresh_instance(instance)

    async def get_instance_by_column(
        self,
        column: InstrumentedAttribute,
        identificator: int | UUID | str,
    ) -> ModelT | None:
        stmt = (
            select(self.model)
            .where(column == identificator)
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    
    async def get_instance_for_update(
        self,
        column: InstrumentedAttribute,
        identificator: int | UUID,
    ) -> ModelT | None:
        stmt = (
            select(self.model)
            .where(column == identificator)
            .with_for_update()
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def update_instance(
        self,
        instance: ModelT,
        data: dict[str, Any]
    ) -> ModelT:
        for key, value in data.items():
            setattr(instance, key, value)   
        
        await self.flush()
        return instance

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

