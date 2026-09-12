from abc import abstractmethod
from typing import Any, Awaitable, Callable, Type, TypeGuard, TypeVar
from uuid import UUID

from Backend.core.interfaces.base_repository_interfaces import (
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService
from Backend.utils.exceptions import Forbidden, NotFound

ModelT = TypeVar("ModelT", bound=Base)
RepoT = TypeVar("RepoT")


class BaseReadEngine(BaseService[ModelT, RepoT]):
    @property
    @abstractmethod
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        pass

    async def _base_fetch(self, id: int) -> ModelT:
        instance = await self.get_func(id)

        if instance is None:
            raise NotFound()

        return instance


class BaseReadPublicService(BaseReadEngine[ModelT, RepoT]):
    async def fetch(self, id: int) -> ModelT:
        return await self._base_fetch(id)


class BaseReadAuthorizedService(BaseReadEngine[ModelT, RepoT]):
    @staticmethod
    def check_user_access(instance: ModelT | None, user_id: UUID) -> TypeGuard[ModelT]:
        return getattr(instance, "user_id", None) == user_id

    async def fetch_authorized(self, id: int, user_id: UUID) -> ModelT:
        instance = await self._base_fetch(id)

        if not self.check_user_access(instance, user_id):
            raise Forbidden()

        return instance
