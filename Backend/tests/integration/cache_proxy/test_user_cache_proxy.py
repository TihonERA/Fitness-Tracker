import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.UserCacheProxy import UserCacheProxy
from Backend.models.user import User
from Backend.schemas.user import UserCachePrefixes, UserUpdateDTO
from Backend.utils.uow import UnitOfWork

@pytest.mark.asyncio(loop_scope="session")
class TestUserCacheProxy:

    @pytest.fixture
    def proxy(self, uow: UnitOfWork, redis: Redis):
        return UserCacheProxy(uow=uow, redis=redis)

    @pytest.fixture
    async def by_id_login_email_cache(self, user: User, proxy: UserCacheProxy):
        redis = proxy.redis

        await proxy.get_user_by_id(user.id)
        await proxy.get_user_by_email(user.email)
        await proxy.get_user_by_login(user.login)

        user_by_id_pattern = UserCachePrefixes.user_by_id + ":*"
        user_by_login_pattern = UserCachePrefixes.user_by_login + ":*"
        user_by_email_pattern = UserCachePrefixes.user_by_email + ":*"

        user_by_id_key = [
            key
            async for key in redis.scan_iter(match=user_by_id_pattern)
        ]
        user_by_login_key = [
            key
            async for key in redis.scan_iter(match=user_by_login_pattern)
        ]
        user_by_email_key = [
            key
            async for key in redis.scan_iter(match=user_by_email_pattern)
        ]

        return {
            "user_id": user.id,
            "user_by_id_key": len(user_by_id_key),
            "user_by_login_key": len(user_by_login_key),
            "user_by_email_key": len(user_by_email_key)
        }

    async def test_get_user_by_column(
        self,
        by_id_login_email_cache
    ):
        assert by_id_login_email_cache.get("user_by_id_key") > 0
        assert by_id_login_email_cache.get("user_by_login_key") > 0
        assert by_id_login_email_cache.get("user_by_email_key") > 0

    async def test_update_user(
        self,
        proxy: UserCacheProxy,
        user: User
    ):
        redis: Redis = proxy.redis

        await proxy.get_user_by_id(user_id=user.id)

        data = UserUpdateDTO(
            login="newlogin"
        )

        await proxy.update_user(user_id=user.id, data=data)

        user_by_id_pattern = UserCachePrefixes.user_by_id + ":*"

        user_by_id_key = [
            key
            async for key in redis.scan_iter(match=user_by_id_pattern)
        ]

        assert user_by_id_key == []

    async def test_delete_user(
        self,
        proxy: UserCacheProxy,
        by_id_login_email_cache
    ):
        redis: Redis = proxy.redis

        await proxy.delete_user(user_id=by_id_login_email_cache.get("user_id"))

        assert by_id_login_email_cache.get("user_by_id_key") > 0
        assert by_id_login_email_cache.get("user_by_login_key") > 0
        assert by_id_login_email_cache.get("user_by_email_key") > 0
