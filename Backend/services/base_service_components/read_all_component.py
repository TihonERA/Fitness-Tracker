from typing import Sequence
from uuid import UUID

from pydantic import BaseModel

from Backend.core.interfaces.base_repository_interfaces import (
    BaseReadAllRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService


class ReadAllAuthorizedService[
    ModelT: Base,
    RepoT: BaseReadAllRepositoryInterface,
    SchemaT: BaseModel,
    SchemaDTOT: BaseModel,
](BaseService[ModelT, RepoT]):
    def __init__(self, dto_scheme: type[SchemaDTOT]) -> None:
        self.dto_scheme = dto_scheme

    async def fetch_all(self, user_id: UUID, data: SchemaT) -> Sequence[ModelT]:
        dto = self.dto_scheme(user_id=user_id, **data)

        instances = await self.repository.get_all(dto)

        if not instances:
            return []

        return instances
