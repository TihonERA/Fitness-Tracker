from typing import Awaitable, Callable, ParamSpec, TypeVar

from sqlalchemy.util import get_func_kwargs

from Backend.core.interfaces.base_repository_interfaces import (
    BaseLockRepositoryInterface,
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.read_components.components import (
    BaseReadAuthorizedService,
    BaseReadPublicService,
)
from Backend.services.base_service_components.interfaces import (
    ReadAuthorizedServiceInterface,
    ReadLockAuthorizedServiceInterface,
    ReadLockPublicServiceInterface,
    ReadRelationAuthorizedServiceInterface,
)

ModelT = TypeVar("ModelT", bound=Base)
RepoT = TypeVar("RepoT")


ReadRepoT = TypeVar("ReadRepoT", bound=BaseReadRepositoryInterface)


class ReadPublicService(BaseReadPublicService[ModelT, ReadRepoT]):
    @property
    def _get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get


ReadRelationRepoT = TypeVar(
    "ReadRelationRepoT", bound=BaseReadRelationRepositoryInterface
)


class ReadRelationAuthorizedService(
    BaseReadAuthorizedService[ModelT, ReadRelationRepoT],
    ReadRelationAuthorizedServiceInterface[ModelT],
):
    @property
    def _get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get_loaded


BaseLockRepoT = TypeVar("BaseLockRepoT", bound=BaseLockRepositoryInterface)


class ReadLockAuthorizedService(
    BaseReadAuthorizedService[ModelT, BaseLockRepoT],
    ReadLockAuthorizedServiceInterface[ModelT],
):
    @property
    def _get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get_for_update


class ReadLockPublicService(
    BaseReadPublicService[ModelT, BaseLockRepoT], ReadLockPublicServiceInterface[ModelT]
):
    @property
    def _get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get_for_update
