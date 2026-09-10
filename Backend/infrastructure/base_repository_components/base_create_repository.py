from typing import Sequence

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base
from Backend.utils.exceptions import DBErrorHandler


class BaseCreateRepository[ModelT: Base](BaseRepository[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.model = model
        super().__init__(session)

    async def create(self, data: BaseModel) -> ModelT:
        try:
            instance = self.model(**data.model_dump(exclude_unset=True))
            return await self._add_and_refresh_instance(instance)
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)
