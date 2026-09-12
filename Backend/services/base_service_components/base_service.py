from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel

from Backend.models.base import Base, ModelT
from Backend.models.user import User
from Backend.utils.exceptions import Forbidden, NotFound

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Any, Awaitable, Callable, Coroutine, Sequence, TypeGuard, TypeVar


class BaseService[ModelT: Base, RepoT]:
    @property
    @abstractmethod
    def repository(self) -> RepoT:
        pass

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
