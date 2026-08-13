from uuid import UUID

from pydantic import BaseModel
from pydantic.functional_validators import ModelAfterValidator

from Backend.models.base import ModelT
from Backend.utils.exceptions import Forbidden, NotFound

from ..utils.uow import UnitOfWork

from typing import Any, Awaitable, Callable, Coroutine, TypeGuard, TypeVar

from Backend.repositories.SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

from redis.asyncio import Redis

class BaseService:

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    async def _get_existing_instance(
        self,
        identifier: int | UUID | str,
        repo_get_func: Callable[[Any], Awaitable[ModelT | None]]
    ) -> ModelT:
        instance = await repo_get_func(identifier)

        if instance is None:
            raise NotFound()

        return instance

    async def _get_instance_with_access(
        self,
        identifier: int | UUID | str, 
        user_id: UUID,
        repo_get_func: Callable[[Any], Awaitable[ModelT | None]]
    ) -> ModelT:
        instance = await self._get_existing_instance(
            identifier=identifier,
            repo_get_func=repo_get_func
        )
        if not self.check_access(instance, user_id):
            raise Forbidden()

        return instance

    @staticmethod
    def check_access(
        instance: ModelT | None, 
        user_id: UUID
    ) -> TypeGuard[ModelT]:
        user_id_column = getattr(instance, "user_id", None)
        
        if user_id_column != user_id:
            return False

        return True
