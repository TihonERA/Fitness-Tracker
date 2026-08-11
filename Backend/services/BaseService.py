from uuid import UUID

from Backend.core.cache_service import CacheService
from Backend.models.base import ModelT

from ..utils.uow import UnitOfWork

from typing import Any, TypeGuard

from redis.asyncio import Redis

class BaseService:

    def __init__(
        self,
        uow: UnitOfWork,
        redis: Redis 
    ) -> None:
        self.uow = uow
        self.cache_service = CacheService(redis=redis)

    @staticmethod
    def check_if_instaces_is_not_none(*args: ModelT | None) -> TypeGuard[ModelT]:
        for instance in args:
            if instance is None:
                return False
        return True

    @staticmethod
    def check_if_user_have_access(
        instance: ModelT | None, 
        user_id: UUID
    ) -> TypeGuard[ModelT]:
        user_id_column = getattr(instance, "user_id", None)
        
        if user_id_column != user_id:
            return False

        return True
