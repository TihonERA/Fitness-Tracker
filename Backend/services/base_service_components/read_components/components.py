from abc import abstractmethod
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    ParamSpec,
    Type,
    TypeGuard,
    TypeVar,
)
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
    def _get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        pass

    async def _base_fetch(self, id: int) -> ModelT:
        instance = await self._get_func(id)

        if instance is None:
            raise NotFound()

        return instance


class BaseReadPublicService(BaseReadEngine[ModelT, RepoT]):
    async def fetch(self, id: int) -> ModelT:
        return await self._base_fetch(id)


class BaseReadAuthorizedService(BaseReadEngine[ModelT, RepoT], Generic[ModelT, RepoT]):
    @property
    @abstractmethod
    def auth_validation_func(self) -> Callable[..., bool]:
        pass

    async def fetch_authorized(self, *, id: int, **kwargs: Any) -> ModelT:
        instance = await self._base_fetch(id)

        if not self.auth_validation_func(instance, **kwargs):
            raise Forbidden()

        return instance
