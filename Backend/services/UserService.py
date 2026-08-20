from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models import workout
from Backend.models.user import User
from Backend.repositories.UserRepository import UserRepository
from Backend.schemas.user import UserCachePrefixes, UserCreateDB, UserResponse, UserUpdate, UserUpdateDTO
from Backend.schemas.workout import WorkoutResponse
from Backend.services.BaseService import BaseService
from Backend.utils.exceptions import DBErrorHandler, InternalServerError, InvalidCredentials, NotFound
from Backend.utils.uow import UnitOfWork


class UserService(BaseService[User]):

    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)

    async def create_user(
        self,
        data: UserCreateDB
    ) -> User:
        async with self.uow as uow:
            return await uow.user.create_instance(
                data=data
            )

    async def get_user_by_id(self, user_id: UUID) -> User:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=user_id,
                repo_get_func=uow.user.get_instance_by_id
            )

    async def get_user_by_login(self, login: str) -> User:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=login,
                repo_get_func=uow.user.get_user_by_login
            )

    async def get_user_by_email(self, email: str) -> User:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=email,
                repo_get_func=uow.user.get_user_by_email
            )

    async def check_if_user_exists(
        self,
        login: str,
        email: str
    ) -> User | None:
        async with self.uow as uow:
            return await uow.user.check_user_exists(
                login=login,
                email=email
            )

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdateDTO
    ) -> User:
        async with self.uow as uow:
            return await self.update_instance(
                user_id=user_id,
                id=user_id,
                data=data,
                repo=uow.user
            )

    async def delete_user(
        self,
        user_id: UUID
    ) -> User:
        async with self.uow as uow:
            return await self.delete_instance_with_access(
                user_id=user_id,
                id=user_id,
                repo=uow.user
            )
