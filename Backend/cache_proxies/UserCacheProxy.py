from functools import partial
from uuid import UUID

from Backend.cache_proxies.CacheBaseProxy import CacheBaseProxy
from Backend.cache_proxies.invalidators.CacheUserInvalidator import CacheUserInvalidator
from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import UserCacheKeyFormatter
from Backend.models.user import User
from Backend.schemas.user import UserCachePrefixes, UserCreateDB, UserResponse, UserUpdate, UserUpdateDTO
from Backend.services.UserService import UserService
from Backend.utils.uow import UnitOfWork

from redis.asyncio import Redis

class UserCacheProxy(CacheBaseProxy):
    def __init__(
        self, 
        service: UserService, 
        redis: Redis, 
        invalidator: CacheUserInvalidator,
        formatter: UserCacheKeyFormatter
    ) -> None:
        self.service = service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis=redis, scheme=UserResponse)


    async def create_user(self, data: UserCreateDB) -> User:
        return await self.service.create_user(data=data)

    async def get_user_by_id(self, user_id: UUID) -> str:
        key = self.formatter.get_user_by_id_key(user_id)

        return await self._wrap_cache(
            key=key,
            db_func=partial(self.service.get_user_by_id, user_id)
        )

    async def get_user_by_login(self, login: str) -> User | str:
        key = self.formatter.get_user_by_login_key(login)

        if uuid := await self.get(key):
            return await self.get_user_by_id(user_id=UUID(uuid))

        user = await self.service.get_user_by_login(login=login)

        await self.set(key=key, value=str(user.id))

        return user

    async def get_user_by_email(self, email: str) -> User | str:
        key = self.formatter.get_user_by_email(email)

        if uuid := await self.get(key):
            return await self.get_user_by_id(UUID(uuid))

        user = await self.service.get_user_by_email(email=email)

        await self.set(key=key, value=str(user.id))

        return user

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdateDTO
    ) -> User:
        user = await self.service.update_user(
            user_id=user_id, 
            data=data
        )

        await self.invalidator.invalidate_get_user_by_id(user_id)

        return user

    async def delete_user(
        self,
        user_id: UUID
    ) -> User:
        user = await self.service.delete_user(user_id=user_id)

        await self.invalidator.invalidate_all(
            user_id=user.id,
            login=user.login,
            email=user.email
        )

        return user

