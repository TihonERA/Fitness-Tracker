from typing import Sequence
from uuid import UUID

from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)

from sqlalchemy import ColumnElement, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from Backend.models.base import Base


class BaseReadRepository[ModelT: Base](BaseRepository[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.model = model
        self.pk_column = inspect(self.model).columns.primary_key[0]
        super().__init__(session)

    # Метод - конструктор, для создания специфических селект запросов
    async def get_instance_by_column(
        self,
        column: InstrumentedAttribute | ColumnElement,
        search_value: int | UUID | str,
        options: Sequence[ORMOption] | None = None,
    ) -> ModelT | None:
        stmt = select(self.model).where(column == search_value)

        return await self._scalar_one_or_none(stmt)

    async def get(self, id: int | UUID) -> ModelT | None:
        return await self.get_instance_by_column(column=self.pk_column, search_value=id)
