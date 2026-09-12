from uuid import UUID

from sqlalchemy import delete, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.core.interfaces.base_repository_interfaces import (
    BaseDeleteRepositoryInterface,
)
from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base
from Backend.utils.exceptions import DBErrorHandler


class BaseDeleteRepository[ModelT: Base](
    BaseRepository[ModelT], BaseDeleteRepositoryInterface[ModelT]
):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.model = model
        self.pk_column = inspect(self.model).primary_key[0]
        super().__init__(session)

    async def delete(self, instance: ModelT) -> None:
        try:
            await self.session.delete(instance)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)
