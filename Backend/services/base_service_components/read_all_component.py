from typing import Sequence

from pydantic import BaseModel

from Backend.core.interfaces.base_repository_interfaces import (
    BaseReadAllRepositoryInterface,
)
from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.base_service import BaseService


class ReadAllService[
    ModelT: Base,
    RepoT: BaseReadAllRepositoryInterface,
    SchemaT: BaseModel,
](BaseService[ModelT, RepoT]):
    async def fetch_all(self, data: SchemaT) -> Sequence[ModelT]:
        instances = await self.repository.get_all(data)

        if not instances:
            return []

        return instances
