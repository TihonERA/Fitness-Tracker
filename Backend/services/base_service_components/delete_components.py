from abc import abstractmethod
from typing import Awaitable, Callable
from uuid import UUID

from Backend.core.interfaces.base_repository_interfaces import (
    BaseDeleteRepositoryInterface,
)
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService
from Backend.services.base_service_components.interfaces import (
    DeleteAuthorizedServiceInterface,
    ReadLockAuthorizedServiceInterface,
    ReadLockPublicServiceInterface,
)


class BaseDeleteEngine[ModelT: Base, RepoT: BaseDeleteRepositoryInterface](
    BaseService[ModelT, RepoT]
):
    @property
    @abstractmethod
    def fetch_func(self) -> Callable[..., Awaitable[ModelT]]:
        pass

    async def delete(self, **id_kwargs) -> None:
        instance = await self.fetch_func(**id_kwargs)

        await self.repository.delete(instance)


class DeleteAuthorizedService[ModelT: Base, RepoT: BaseDeleteRepositoryInterface](
    BaseDeleteEngine[ModelT, RepoT], DeleteAuthorizedServiceInterface[ModelT]
):
    def __init__(
        self, read_lock_auth_service: ReadLockAuthorizedServiceInterface[ModelT]
    ) -> None:
        self.read_lock_auth_service = read_lock_auth_service

    @property
    def fetch_func(self) -> Callable[[int, UUID], Awaitable[ModelT]]:
        return self.read_lock_auth_service.fetch_authorized


class DeletePublicService[ModelT: Base, RepoT: BaseDeleteRepositoryInterface](
    BaseDeleteEngine[ModelT, RepoT]
):
    def __init__(
        self, read_lock_public_service: ReadLockPublicServiceInterface[ModelT]
    ) -> None:
        self.read_lock_public_service = read_lock_public_service

    @property
    def fetch_func(self) -> Callable[[int], Awaitable[ModelT]]:
        return self.read_lock_public_service.fetch
