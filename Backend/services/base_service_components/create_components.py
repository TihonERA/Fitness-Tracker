from uuid import UUID

from pydantic import BaseModel

from Backend.core.interfaces.base_repository_interfaces import (
    BaseCreateRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService


class CreateService[
    ModelT: Base,
    RepoT: BaseCreateRepositoryInterface,
    SchemaT: BaseModel,
](BaseService[ModelT, RepoT]):
    async def create(self, data: SchemaT) -> ModelT:
        return await self.repository.create(data)


class RegisterService[
    ModelT: Base,
    RepoT: BaseCreateRepositoryInterface,
    SchemaT: BaseModel,
    SchemaDTOT: BaseModel,
](BaseService[ModelT, RepoT]):
    def __init__(self, dto_scheme: type[SchemaDTOT]) -> None:
        self.dto_scheme = dto_scheme

    async def create(self, user_id: UUID, data: SchemaT) -> ModelT:
        dto = self.dto_scheme(user_id=user_id, **data.model_dump(exclude_unset=True))
        return await self.repository.create(dto)
