from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidators import BaseCacheInvalidator

from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import UserCacheKeyFormatter
from Backend.schemas.user import UserCachePrefixes


class CacheUserInvalidator(BaseCacheInvalidator[UserCacheKeyFormatter]):
    def __init__(self, redis: Redis, formatter: UserCacheKeyFormatter) -> None:
        self.pref = UserCachePrefixes
        super().__init__(redis, formatter)

    async def invalidate_get_user_by_id(self, user_id: UUID) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)

        await self.redis.delete(user_by_id_key)

    async def invalidate_all(
        self,
        user_id: UUID,
        login: str,
        email: str
    ) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)
        user_by_login_key = self.formatter.get_user_by_login_key(login)
        user_by_email_key = self.formatter.get_user_by_email(email)

        await self.redis.delete(user_by_id_key, user_by_login_key, user_by_email_key)
