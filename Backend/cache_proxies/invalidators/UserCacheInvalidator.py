import logging
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator

from Backend.cache_proxies.key_formatters.UserCacheKeyFormatter import (
    UserCacheKeyFormatter,
)
from Backend.schemas.user import UserCachePrefixes
from Backend.utils.decorators import cache_invalidation_logger

logger = logging.Logger(__name__)


class UserCacheInvalidator(BaseCacheInvalidator[UserCacheKeyFormatter]):
    def __init__(self, redis: Redis, formatter: UserCacheKeyFormatter) -> None:
        self.pref = UserCachePrefixes
        super().__init__(redis, formatter)

    @cache_invalidation_logger(logger)
    async def invalidate_get_user_by_id(self, user_id: UUID) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)

        await self.redis.delete(user_by_id_key)

    @cache_invalidation_logger(logger)
    async def _invalidate_by_field(self, user_id: UUID, key: str) -> None:
        tag_key = self.formatter.get_tag_key(user_id)

        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.delete(key)

            await pipe.srem(tag_key, key)

    @cache_invalidation_logger(logger)
    async def invalidate_get_user_by_login(
        self, user_id: UUID, old_login_key: str, new_login_key: str
    ) -> None:
        await self._invalidate_by_field(user_id=user_id, key=old_login_key)

    @cache_invalidation_logger(logger)
    async def invalidate_get_user_by_email(
        self, user_id: UUID, old_email_key: str, new_email_key: str
    ) -> None:
        await self._invalidate_by_field(user_id=user_id, key=old_email_key)

    @cache_invalidation_logger(logger)
    async def invalidate_all(self, user_id: UUID) -> None:
        user_by_id_key = self.formatter.get_user_by_id_key(user_id)
        tag_key = self.formatter.get_tag_key(user_id)

        raw_bound_keys = await self.redis.smembers(tag_key)
        bound_keys = [
            k.decode("utf-8") if isinstance(k, bytes) else k for k in raw_bound_keys
        ]

        keys_to_delete = [user_by_id_key, *bound_keys]

        async with self.redis.pipeline() as pipe:
            pipe.delete(*keys_to_delete)
            pipe.srem(tag_key, *keys_to_delete)

            await pipe.execute()
