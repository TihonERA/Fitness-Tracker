import pytest

from Backend.cache_proxies.CacheBaseProxy import CacheBaseProxy

@pytest.mark.asyncio(loop_scope="session")
class TestCacheBaseProxy:

    @pytest.fixture
    def service(self, mocker):
        return CacheBaseProxy(redis=mocker.AsyncMock(), scheme=mocker.Mock())

    async def test_formate_key_flat_args(self, service: CacheBaseProxy):
        key = service.formate_key(
            prefix="workout:all",
            user_id="0000",
            workout_id=-1
        )

        assert key == "workout:all:user_id=0000:workout_id=-1"

    async def test_formate_key_sorting_stability(self, service: CacheBaseProxy):
        key1 = service.formate_key(
            prefix="workout:all",
            user_id="0000",
            workout_id=-1
        )

        key2 = service.formate_key(
            workout_id=-1,
            prefix="workout:all",
            user_id="0000"
        )

        assert key1 == key2

    async def test_formate_key_nested_dict(self, service: CacheBaseProxy):
        key = service.formate_key(
            prefix="workout:all",
            filter={
                "name": "workoutnew",
                "description": "description"
            }
        )

        assert key == "workout:all:description=description:name=workoutnew"
