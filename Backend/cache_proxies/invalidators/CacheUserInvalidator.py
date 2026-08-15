from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.CacheKeyFormatter import CacheKeyFormatter
from Backend.cache_proxies.invalidators.BaseCacheInvalidators import BaseCacheInvalidator

from Backend.schemas.user import UserCachePrefixes


class CacheUserInvalidator(BaseCacheInvalidator):
    def __init__(self, redis: Redis, formatter: CacheKeyFormatter) -> None:
        self.pref = UserCachePrefixes
        super().__init__(redis, formatter)

    def _formate_get_user_by_id_key(self, user_id: UUID) -> str:
        user_by_id_key = self.formatter.formate_key(
            prefix=self.pref.user_by_id,
            user_id=user_id
        )

        return user_by_id_key

    async def invalidate_get_user_by_id(self, user_id: UUID) -> None:
        user_by_id_key = self._formate_get_user_by_id_key(user_id)

        await self.redis.delete(user_by_id_key)

    async def invalidate_all(
        self,
        user_id: UUID,
        login: str,
        email: str
    ) -> None:
        user_by_id_key = self._formate_get_user_by_id_key(user_id)
        user_by_login_key = self.formatter.formate_key(
            prefix=self.pref.user_by_login,
            login=login
        )
        user_by_email_key = self.formatter.formate_key(
            prefix=self.pref.user_by_email,
            email=email
        )

        await self.redis.delete(user_by_id_key, user_by_login_key, user_by_email_key)
