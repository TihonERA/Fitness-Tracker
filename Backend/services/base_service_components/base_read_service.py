from abc import abstractmethod
from typing import Awaitable, Callable
from uuid import UUID

from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.infrastructure.base_repository_components.base_read_repository import (
    BaseReadRepository,
)
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService
from Backend.utils.exceptions import Forbidden, NotFound


class BaseReadService[ModelT, RepoT](BaseService[ModelT, RepoT]):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @property
    @abstractmethod
    def get_func(self) -> Callable[[int | UUID], Awaitable[ModelT | None]]:
        pass

    async def _fetch_and_verify_existense(self, id: int) -> ModelT:
        instance = await self.get_func(id)

        if instance is None:
            raise NotFound()

        return instance
