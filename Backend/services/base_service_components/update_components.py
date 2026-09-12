from abc import abstractmethod
from typing import Awaitable, Callable, Generic, ParamSpec, Type, TypeVar
from uuid import UUID
import uuid

from pydantic import BaseModel

from Backend.core.interfaces.base_repository_interfaces import (
    BaseLockRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService
from Backend.services.base_service_components.read_components.mixins import (
    ReadLockAuthorizedService,
)
from Backend.services.base_service_components.interfaces import (
    ReadLockAuthorizedServiceInterface,
    ReadLockPublicServiceInterface,
)


class BaseUpdateEngine[
    ModelT: Base, RepoT: BaseUpdateRepositoryInterface, SchemaT: BaseModel, **P
](BaseService[ModelT, RepoT]):
    @property
    @abstractmethod
    def fetch_func(self) -> Callable[P, Awaitable[ModelT]]:
        pass

    async def update(
        self, data: SchemaT, *id_args: P.args, **id_kwargs: P.kwargs
    ) -> ModelT:
        instance = await self.fetch_func(*id_args, **id_kwargs)

        return await self.repository.update(instance, data)


class UpdatePublicService[
    ModelT: Base, RepoT: BaseUpdateRepositoryInterface, SchemaT: BaseModel
](BaseUpdateEngine[ModelT, RepoT, SchemaT, [int]]):
    def __init__(
        self, read_lock_public_service: ReadLockPublicServiceInterface[ModelT]
    ) -> None:
        self.read_lock_public_service = read_lock_public_service

    @property
    def fetch_func(self) -> Callable[[int], Awaitable[ModelT]]:
        return self.read_lock_public_service.fetch


class UpdateAuthorizedService[
    ModelT: Base, RepoT: BaseUpdateRepositoryInterface, SchemaT: BaseModel
](BaseUpdateEngine[ModelT, RepoT, SchemaT, [int, UUID]]):
    def __init__(
        self, read_lock_auth_service: ReadLockAuthorizedServiceInterface[ModelT]
    ) -> None:
        self.read_lock_auth_service = read_lock_auth_service

    @property
    def fetch_func(self) -> Callable[[int, UUID], Awaitable[ModelT]]:
        return self.read_lock_auth_service.fetch_authorized
