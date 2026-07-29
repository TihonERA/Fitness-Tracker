from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.user import User
from Backend.repositories.UserRepository import UserRepository
from Backend.schemas.user import UserCreateDB, UserResponse, UserUpdate
from Backend.utils.decorators import cache, invalidate_cache
from Backend.utils.validators import NotFound


class UserService:

    def __init__(self, session: AsyncSession, redis: Redis):
        self.userrepo = UserRepository(session=session)
        self.redis = redis

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
        if not user:
            raise NotFound()
        return user

    async def get_user_by_login(self, login: str) -> User:
        user = await self.userrepo.get_user_by_login(login=login)
        if not user:
            raise NotFound()
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.userrepo.get_user_by_email(email=email)
        if not user:
            raise NotFound()
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
        result = await self.userrepo.update_user(
            user_id=user_id,
            data=data.model_dump(exclude_unset=True)
        )
        if result is None:
            raise NotFound()

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
