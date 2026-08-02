from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.user import User
from Backend.repositories.UserRepository import UserRepository
from Backend.schemas.user import UserCreateDB, UserResponse, UserUpdate
from Backend.services.BaseService import BaseService
from Backend.utils.decorators import cache, invalidate_cache
from Backend.utils.exceptions import InternalServerError, InvalidCredentials, NotFound
from Backend.utils.uow import UnitOfWork


class UserService(BaseService):

    def __init__(self, uow: UnitOfWork, redis: Redis):
        self.userrepo = uow.user
        super().__init__(uow, redis)

    async def create_user(
        self,
        data: UserCreateDB
    ) -> User:
        return await self.userrepo.create_user(
            data=data.model_dump()
        )

    @cache(ttl=timedelta(hours=12), column=User.user_id, schema=UserResponse)
    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.userrepo.get_user_by_id(user_id=user_id)

        user, = self.check_if_instaces_is_none_returning_tuple(user)
        return user

    async def get_user_by_login(self, login: str) -> User:
        user = await self.userrepo.get_user_by_login(login=login)

        user, = self.check_if_instaces_is_none_returning_tuple(user)
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.userrepo.get_user_by_email(email=email)

        user, = self.check_if_instaces_is_none_returning_tuple(user)
        return user
    
    async def check_if_user_exists(
        self,
        login: str,
        email: str
    ) -> User | None:
        return await self.userrepo.check_user_exists(
            login=login,
            email=email
        )

    @invalidate_cache(column=User.user_id)
    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdate
    ) -> User:
        user = await self.userrepo.get_user_for_update(
            user_id=user_id,
        )
        if user is None:
            raise NotFound()
        try:
            result = await self.userrepo.update_instance(
                instance=user,
                data=data.model_dump(exclude_unset=True)
            )
        except AttributeError as e:
            raise InternalServerError(
                detail=f"Table: {user.__tablename__} dont have attribute {e.name}, that was declared at a pydantic model"
            )

        return result

    @invalidate_cache(column=User.user_id)
    async def delete_user(
        self,
        user_id: UUID
    ) -> User:
        user =  await self.get_user_by_id(user_id=user_id)
        await self.userrepo.delete_user(
            user_id=user_id
        )

        return user
