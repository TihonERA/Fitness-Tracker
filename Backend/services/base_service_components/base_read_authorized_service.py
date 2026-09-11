from typing import TypeGuard
from uuid import UUID

from Backend.core.interfaces.uow import BaseUOWInterface
from Backend.models.base import Base
from Backend.services.base_service_components.base_read_service import BaseReadService
from Backend.utils.exceptions import Forbidden


class BaseReadAuthorizedService[ModelT, RepoT](BaseReadService[ModelT, RepoT]):
    def __init__(self, uow: BaseUOWInterface) -> None:
        super().__init__(uow)

    @staticmethod
    def check_user_access(instance: ModelT | None, user_id: UUID) -> TypeGuard[ModelT]:
        instance_user_id = getattr(instance, "user_id", None)

        if instance_user_id != user_id:
            return False

        return True

    async def _fetch_authorized(self, id: int, user_id: UUID) -> ModelT:
        instance = await self._fetch_and_verify_existense(id)

        if not self.check_user_access(instance, user_id):
            raise Forbidden()

        return instance
