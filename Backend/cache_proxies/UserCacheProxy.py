from functools import partial
from uuid import UUID

from Backend.cache_proxies.CacheBaseProxy import CacheBaseProxy
from Backend.models.user import User
from Backend.schemas.user import UserCachePrefixes, UserCreateDB, UserResponse, UserUpdate, UserUpdateDTO
from Backend.services.UserService import UserService
from Backend.utils.uow import UnitOfWork

from redis.asyncio import Redis

class UserCacheProxy(CacheBaseProxy[User]):
    def __init__(self, uow: UnitOfWork, redis: Redis) -> None:
        self.user_service = UserService(uow=uow)
        super().__init__(redis, UserResponse)

    async def create_user(self, data: UserCreateDB) -> User:
        return await self.user_service.create_user(data=data)

    async def get_user_by_id(self, user_id: UUID) -> str:
        key = self.formate_key(
            prefix=UserCachePrefixes.user_by_id,
            user_id=user_id
        )

        get_user_by_id = partial(
            self.user_service.get_user_by_id,
            user_id=user_id
        )

        return await self._wrap_cache(
            key=key,
            db_func=get_user_by_id
        )

    async def get_user_by_login(self, login: str) -> User | str:
        key = self.formate_key(
            prefix=UserCachePrefixes.user_by_login, 
            login=login
        )

        if uuid := await self.get(key):
            return await self.get_user_by_id(user_id=UUID(uuid))

        user = await self.user_service.get_user_by_login(login=login)

        await self.set(key=key, value=str(user.id))

        return user

    async def get_user_by_email(self, email: str) -> User | str:
        key = self.formate_key(
            prefix=UserCachePrefixes.user_by_email,
            email=email
        )

        if uuid := await self.get(key):
            return await self.get_user_by_id(UUID(uuid))

        user = await self.user_service.get_user_by_email(email=email)

        await self.set(key=key, value=str(user.id))

        return user

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdateDTO
    ) -> User:
        user = await self.user_service.update_user(
            user_id=user_id, 
            data=data
        )

        user_by_id_key = self.formate_key(
            prefix=UserCachePrefixes.user_by_id,
            user_id=user_id
        )

        await self.redis.delete(user_by_id_key)

        return user

    async def delete_user(
        self,
        user_id: UUID
    ) -> User:
        user = await self.user_service.delete_user(user_id=user_id)


        keys = [
            self.formate_key(
                prefix=UserCachePrefixes.user_by_id,
                user_id=user_id
            ),
            self.formate_key(
                prefix=UserCachePrefixes.user_by_login,
                login=user.login
            ),
            self.formate_key(
                prefix=UserCachePrefixes.user_by_email,
                email=user.email
            )
        ]

        await self.redis.delete(*keys)

        return user

