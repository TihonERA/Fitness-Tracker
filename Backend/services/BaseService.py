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

    async def _get_instance_and_validate(
        self,
        id: int, 
        user_id: UUID,
        repo_get_func: Callable[[int], Awaitable]
    ):
        instance = await repo_get_func(id)

        if instance is None:
            raise NotFound()

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
