from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import ColumnElement, delete, inspect, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Generic, Sequence, Any

from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from Backend.utils.exceptions import DBErrorHandler, DBSchemaMismatchError
from Backend.models.base import Base, ModelT


class BaseRepository[ModelT: Base]:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _add_and_refresh_instance(
        self, instance: ModelT, attribute_names: Sequence[str] | None = None
    ) -> ModelT:
        self.add(instance)
        await self.flush()
        if attribute_names:
            await self.refresh(instance, attribute_names=attribute_names)
        else:
            await self.refresh(instance)
        return instance

    async def get_instance_for_update(self, id: int | UUID) -> ModelT | None:
        stmt = select(self.model).where(self.pk_column == id).with_for_update()
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def update_instance(self, instance: ModelT, data: BaseModel) -> ModelT:
        data_dump = data.model_dump(exclude_unset=True)
        try:
            for key, value in data_dump.items():
                setattr(instance, key, value)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e=e)

        return instance

    async def delete_by_id(self, id: int | UUID) -> None:
        stmt = delete(self.model).where(self.pk_column == id)
        result = await self.execute(stmt)

    def add(self, instance: object, **kwargs) -> None:
        self.session.add(instance, **kwargs)

    async def refresh(self, instance: object, **kwargs) -> None:
        await self.session.refresh(instance, **kwargs)

    async def execute(self, stmt, **kwargs):
        return await self.session.execute(stmt, **kwargs)

    async def _scalar_one_or_none(self, stmt):
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def flush(self, instance: Sequence[Any] | None = None) -> None:
        await self.session.flush(instance)
