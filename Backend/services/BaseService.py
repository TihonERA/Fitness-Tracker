from uuid import UUID

from pydantic import BaseModel
from pydantic.functional_validators import ModelAfterValidator

from Backend.models.base import ModelT
from Backend.utils.exceptions import Forbidden, NotFound

from ..utils.uow import UnitOfWork

from typing import Any, Awaitable, Callable, Coroutine, TypeGuard, TypeVar

from redis.asyncio import Redis

class BaseService:

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    @staticmethod
    def check_access(
        instance: ModelT | None, 
        user_id: UUID
    ) -> TypeGuard[ModelT]:
        user_id_column = getattr(instance, "user_id", None)
        
        if user_id_column != user_id:
            return False

        return True
