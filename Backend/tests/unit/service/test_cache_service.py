import pytest

from Backend.core.cache_service import CacheService

@pytest.mark.asyncio(loop_scope="session")
class TestCacheService:

    @pytest.fixture
    def service(self, mocker):
        return CacheService(redis=mocker.AsyncMock())

    async def test_formate_key_flat_args(self, service: CacheService):
        key = service.formate_key(
            prefix="workout:all",
            user_id="0000",
            workout_id=-1
        )

        assert key == "workout:all:user_id=0000:workout_id=-1"

    async def test_formate_key_sorting_stability(self, service: CacheService):
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

    async def test_formate_key_nested_dict(self, service: CacheService):
        key = service.formate_key(
            prefix="workout:all",
            filter={
                "name": "workoutnew",
                "description": "description"
            }
        )

        assert key == "workout:all:description=description:name=workoutnew"
