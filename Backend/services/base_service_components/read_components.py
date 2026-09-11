from abc import abstractmethod
from typing import Any, Awaitable, Callable, Type, TypeGuard
from uuid import UUID

from Backend.core.interfaces.base_repository_interfaces import (
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.services.base_service_components.base_service import BaseService
from Backend.utils.exceptions import Forbidden, NotFound


class BaseReadService[ModelT, RepoT](BaseService[ModelT, RepoT]):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @property
    @abstractmethod
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        pass

    async def _fetch_and_verify_existense(self, id: int) -> ModelT:
        instance = await self.get_func(id)

        if instance is None:
            raise NotFound()

        return instance


class BaseReadAuthorizedService[ModelT, RepoT](BaseReadService[ModelT, RepoT]):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @staticmethod
    def check_user_access(instance: ModelT | None, user_id: UUID) -> TypeGuard[ModelT]:
        return getattr(instance, "user_id", None) == user_id

    async def fetch_authorized(self, id: int, user_id: UUID) -> ModelT:
        instance = await self._fetch_and_verify_existense(id)

        if not self.check_user_access(instance, user_id):
            raise Forbidden()

        return instance


class ReadService[ModelT, RepoT: BaseReadRepositoryInterface](
    BaseReadService[ModelT, RepoT]
):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @property
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get


class ReadRelationAuthorizedService[ModelT, RepoT: BaseReadRelationRepositoryInterface](
    BaseReadAuthorizedService[ModelT, RepoT]
):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @property
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get_loaded
