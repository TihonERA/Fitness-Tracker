from uuid import UUID

from sqlalchemy import delete, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base


class BaseDeleteRepository[ModelT: Base](BaseRepository[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.model = model
        self.pk_column = inspect(self.model).primary_key[0]
        super().__init__(session)

    async def delete(self, id: int | UUID) -> int:
        stmt = delete(self.model).where(self.pk_column == id)

        result = await self.execute(stmt)
        return result.rowcount  # type: ignore
