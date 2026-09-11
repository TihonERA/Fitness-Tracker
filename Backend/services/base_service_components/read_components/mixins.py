from typing import Awaitable, Callable, TypeVar

from Backend.core.interfaces.base_repository_interfaces import (
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.read_components.components import (
    BaseReadAuthorizedService,
    BaseReadPublicService,
)

ModelT = TypeVar("ModelT", bound=Base)
RepoT = TypeVar("RepoT")
UowT = TypeVar("UowT", bound=BaseUOWInterface)


ReadRepoT = TypeVar("ReadRepoT", bound=BaseReadRepositoryInterface)


class ReadPublicService(BaseReadPublicService[ModelT, ReadRepoT, UowT]):
    def __init__(self, uow: UowT) -> None:
        super().__init__(uow)

    @property
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get


ReadRelationRepoT = TypeVar(
    "ReadRelationRepoT", bound=BaseReadRelationRepositoryInterface
)


class ReadRelationAuthorizedService(
    BaseReadAuthorizedService[ModelT, ReadRelationRepoT, UowT]
):
    def __init__(self, uow: UowT) -> None:
        super().__init__(uow)

    @property
    def get_func(self) -> Callable[..., Awaitable[ModelT | None]]:
        return self.repository.get_loaded
