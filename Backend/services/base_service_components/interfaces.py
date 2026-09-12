from abc import ABC, abstractmethod
from uuid import UUID

from Backend.models.base import Base


class ReadLockAuthorizedServiceInterface[ModelT: Base](ABC):
    @abstractmethod
    async def fetch_authorized(self, id: int, user_id: UUID) -> ModelT:
        pass


class ReadLockPublicServiceInterface[ModelT: Base](ABC):
    @abstractmethod
    async def fetch(self, id: int) -> ModelT:
        pass
