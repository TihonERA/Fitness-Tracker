from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from pydantic import BaseModel

from Backend.models.base import Base


class ReadAuthorizedServiceInterface[ModelT: Base](ABC):
    @abstractmethod
    async def fetch_authorized(self, id: int, user_id: UUID) -> ModelT:
        pass


class ReadRelationAuthorizedServiceInterface[ModelT: Base](
    ReadAuthorizedServiceInterface[ModelT]
):
    pass


class ReadLockAuthorizedServiceInterface[ModelT: Base](
    ReadAuthorizedServiceInterface[ModelT]
):
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
