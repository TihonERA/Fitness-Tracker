from abc import ABC, abstractmethod
from typing import Callable, Sequence, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from Backend.models.base import Base


class ReadAuthorizedServiceInterface[ModelT: Base](ABC):
    @property
    @abstractmethod
    def auth_validation_func(self) -> Callable[..., bool]:
        raise NotImplementedError()


class ReadRelationAuthorizedServiceInterface[ModelT: Base](
    ReadAuthorizedServiceInterface[ModelT]
):
    pass


class ReadLockAuthorizedServiceInterface[ModelT: Base, **P](ABC):
    @abstractmethod
    async def fetch_authorized(self, *args: P.args, **kwargs: P.kwargs) -> ModelT:
        pass


class ReadLockPublicServiceInterface[ModelT: Base](ABC):
    @abstractmethod
    async def fetch(self, id: int) -> ModelT:
        pass


class ReadAllServiceInterface[ModelT: Base, SchemaT: BaseModel](ABC):
    @abstractmethod
    async def fetch_all(self, user_id: UUID, data: SchemaT) -> Sequence[ModelT]:
        pass


class RegisterServiceInterface[ModelT: Base, SchemaT: BaseModel](ABC):
    @abstractmethod
    async def create(self, user_id: UUID, data: SchemaT) -> ModelT:
        pass


class UpdateAuthorizedServiceInterface[ModelT: Base, SchemaT: BaseModel](ABC):
    @abstractmethod
    async def update(self, data: SchemaT, *, id: int, user_id: UUID) -> ModelT:
        pass


class DeleteAuthorizedServiceInterface[ModelT: Base](ABC):
    @abstractmethod
    async def delete(self, *, id: int, user_id: UUID) -> None:
        pass
