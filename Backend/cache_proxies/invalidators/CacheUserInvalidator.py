from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidators import BaseCacheInvalidator

from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import UserCacheKeyFormatter
from Backend.schemas.user import UserCachePrefixes


class UserCacheInvalidator(BaseCacheInvalidator[UserCacheKeyFormatter]):
    def __init__(self, redis: Redis, formatter: UserCacheKeyFormatter) -> None:
        self.pref = UserCachePrefixes
        super().__init__(redis, formatter)

    async def invalidate_get_user_by_id(self, user_id: UUID) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)

        await self.redis.delete(user_by_id_key)

    async def _invalidate_by_field(
        self,
        user_id: UUID,
        old_field_key: str,
        new_field_key: str
    ) -> None:
        tag_key = self.formatter.get_tag_key(user_id)

        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.delete(old_field_key)

            await pipe.srem(tag_key, old_field_key)

    async def invalidate_get_user_by_login(
        self,
        user_id: UUID,
        old_login_key: str,
        new_login_key: str
    ) -> None:
        await self._invalidate_by_field(
            user_id=user_id,
            old_field_key=old_login_key,
            new_field_key=new_login_key
        )

    async def invalidate_get_user_by_email(
        self,
        user_id: UUID,
        old_email_key: str,
        new_email_key: str
    ) -> None:
        await self._invalidate_by_field(
            user_id=user_id,
            old_field_key=old_email_key,
            new_field_key=new_email_key
        )
        
    async def invalidate_all(
        self,
        user_id: UUID
    ) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)
        tag_key = self.formatter.get_tag_key(user_id)

        raw_bound_keys = await self.redis.smembers(tag_key) 
        bound_keys = [
            k.decode("utf-8")
            if isinstance(k, bytes) 
            else k 
            for k in raw_bound_keys
        ]

        keys_to_delete = [user_by_id_key, tag_key, *bound_keys]

        await self.redis.delete(*keys_to_delete)
