from uuid import UUID

from pydantic import BaseModel
from pydantic.functional_validators import ModelAfterValidator

from Backend.models.base import Base, ModelT
from Backend.models.user import User
from Backend.repositories import SqlAlchemyAbstractRepository
from Backend.utils.exceptions import Forbidden, NotFound

from ..utils.uow import UnitOfWork

from typing import Any, Awaitable, Callable, Coroutine, Sequence, TypeGuard, TypeVar

from Backend.repositories.SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

from redis.asyncio import Redis

class BaseService[ModelT: Base]:

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    async def _get_existing_instance(
        self,
        identifier: int | UUID | str,
        repo_get_func: Callable[[Any], Awaitable[ModelT | None]]
    ) -> ModelT:
        instance = await repo_get_func(identifier)

        if instance is None:
            raise NotFound()

        return instance

    async def _get_instance_with_access(
        self,
        identifier: int | UUID | str, 
        user_id: UUID,
        repo_get_func: Callable[[Any], Awaitable[ModelT | None]]
    ) -> ModelT:
        instance = await self._get_existing_instance(
            identifier=identifier,
            repo_get_func=repo_get_func
        )
        if not self.check_access(instance, user_id):
            raise Forbidden()

        return instance

    async def get_all_instances(
        self, 
        data: BaseModel,
        repo_get_all_func: Callable[[Any], Awaitable[Sequence[ModelT]]]
    ) -> Sequence[ModelT]:
            instances = await repo_get_all_func(data)

            if not instances:
                return []

            return instances

    async def delete_instance_with_access(
        self,
        user_id: UUID,
        id: int | UUID,
        repo: SQLAlchemyAbstractRepository
    ) -> ModelT:
        instance = await self._get_instance_with_access(
            identifier=id,
            user_id=user_id,
            repo_get_func=repo.get_instance_for_update
        )

        await repo.delete_by_id(id)

        return instance

    async def update_instance(
        self,
        user_id: UUID,
        id: int | UUID,
        data: BaseModel,
        repo: SQLAlchemyAbstractRepository
    ) -> ModelT:
        instance = await self._get_instance_with_access(
            identifier=id,
            user_id=user_id,
            repo_get_func=repo.get_instance_for_update
        )
        updated_workout = await repo.update_instance(
            instance=instance,
            data=data
        )

        return updated_workout


    @staticmethod
    def check_access(
        instance: ModelT | None, 
        user_id: UUID
    ) -> TypeGuard[ModelT]:
        user_id_column = getattr(instance, "user_id", None)
        
        if user_id_column != user_id and not isinstance(instance, User):
            return False

        return True
