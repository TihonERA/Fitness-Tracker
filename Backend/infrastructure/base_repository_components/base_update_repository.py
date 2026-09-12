from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.lambdas import insp

from Backend.infrastructure.base_repository_components.base_lock_repository import (
    BaseLockRepository,
)
from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base
from Backend.utils.exceptions import DBErrorHandler


class BaseUpdateRepository[ModelT: Base](BaseRepository[ModelT]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelT],
    ) -> None:
        self.model = model
        self.pk_column = inspect(self.model).primary_key[0]
        super().__init__(session)

    async def update(self, instance: ModelT, data: BaseModel) -> ModelT:
        data_dump = data.model_dump(exclude_unset=True)
        try:
            for key, value in data_dump.items():
                setattr(instance, key, value)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)

        return instance
