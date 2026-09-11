from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel

from Backend.models.base import Base, ModelT
from Backend.models.user import User
from Backend.utils.exceptions import Forbidden, NotFound

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Any, Awaitable, Callable, Coroutine, Sequence, TypeGuard, TypeVar

from Backend.infrastructure.SqlAlchemyAbstractRepository import (
    SQLAlchemyAbstractRepository,
)


class BaseService[ModelT, RepoT]:
    def __init__(self, uow: BaseUOWInterface) -> None:
        self.uow = uow

    @property
    @abstractmethod
    def repository(self) -> RepoT:
        pass

    async def get_all_instances(
        self,
        data: BaseModel,
        repo_get_all_func: Callable[[Any], Awaitable[Sequence[ModelT]]],
    ) -> Sequence[ModelT]:
        instances = await repo_get_all_func(data)

        if not instances:
            return []

        return instances

    async def delete_existing_instance(
        self, id: int | UUID, repo: SQLAlchemyAbstractRepository
    ) -> ModelT:
        instance = await self._get_existing_instance(
            identifier=id, repo_get_func=repo.get_instance_for_update
        )

        await repo.delete_by_id(id)

        return instance

    async def delete_instance_with_access(
        self, user_id: UUID, id: int | UUID, repo: SQLAlchemyAbstractRepository
    ) -> ModelT:
        instance = await self._get_instance_with_access(
            identifier=id, user_id=user_id, repo_get_func=repo.get_instance_for_update
        )

        await repo.delete_by_id(id)

        return instance

    async def update_existing_instance(
        self, id: int | UUID, data: BaseModel, repo: SQLAlchemyAbstractRepository
    ) -> ModelT:
        instance = await self._get_existing_instance(
            identifier=id, repo_get_func=repo.get_instance_for_update
        )
        updated_workout = await repo.update_instance(instance=instance, data=data)
        return updated_workout

    async def update_instance_with_access(
        self,
        user_id: UUID,
        id: int | UUID,
        data: BaseModel,
        repo: SQLAlchemyAbstractRepository,
    ) -> ModelT:
        instance = await self._get_instance_with_access(
            identifier=id, user_id=user_id, repo_get_func=repo.get_instance_for_update
        )
        updated_workout = await repo.update_instance(instance=instance, data=data)
        return updated_workout
