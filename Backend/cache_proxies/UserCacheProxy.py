from datetime import timedelta
from functools import partial
from os import wait
from typing import Any, Awaitable, Callable
from uuid import UUID

import json

from pydantic import BaseModel

from Backend.cache_proxies.CacheBaseProxy import BaseCacheProxy 
from Backend.cache_proxies.invalidators.CacheUserInvalidator import UserCacheInvalidator
from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import UserCacheKeyFormatter
from Backend.models.user import User
from Backend.schemas.user import UserCachePrefixes, UserCreateDB, UserResponse, UserUpdate, UserUpdateDTO
from Backend.services.UserService import UserService
from Backend.utils.uow import UnitOfWork

from redis.asyncio import Redis

class UserCacheProxy(BaseCacheProxy[UserResponse]):
    def __init__(
        self, 
        service: UserService, 
        redis: Redis, 
        invalidator: UserCacheInvalidator,
        formatter: UserCacheKeyFormatter
    ) -> None:
        self.service = service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis=redis, scheme=UserResponse)


    async def create_user(self, data: UserCreateDB) -> User:
        return await self.service.create_user(data=data)

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        key = self.formatter.get_user_by_id_key(user_id)

        user = await self._wrap_cache(
            key=key,
            db_func=partial(self.service.get_user_by_id, user_id)
        )

        return user

    async def _get_user_by_field(
        self, 
        field_value: str,
        key_formatter_func: Callable[[str], str],
        service_func: Callable[[str], Awaitable[User]]
    ) -> UserResponse:
        key = key_formatter_func(field_value)

        if uuid := await self.get(key):
            return await self.get_user_by_id(user_id=UUID(uuid))

        user = await service_func(field_value)

        await self.set(key=key, value=str(user.id))

        tag_key = self.formatter.get_tag_key(user.id)
        await self.sadd(key=tag_key, values=key)

        return self.scheme.model_validate(user)

    async def get_user_by_login(self, login: str) -> UserResponse:
        return await self._get_user_by_field(
            field_value=login,
            key_formatter_func=self.formatter.get_user_by_login_key,
            service_func=self.service.get_user_by_login
        )
        
    async def get_user_by_email(self, email: str) -> UserResponse:
        return await self._get_user_by_field(
            field_value=email,
            key_formatter_func=self.formatter.get_user_by_email_key,
            service_func=self.service.get_user_by_email
        )

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdateDTO
    ) -> User:
        user = await self.service.update_user(
            user_id=user_id, 
            data=data
        )

        await self.invalidator.invalidate_all(user_id)

        return user

    async def delete_user(
        self,
        user_id: UUID
    ) -> User:
        user = await self.service.delete_user(user_id)

        await self.invalidator.invalidate_all(user_id)

        return user

