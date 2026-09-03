import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.ExerciseHistoryCacheProxy import ExerciseHistoryCacheProxy
from Backend.cache_proxies.invalidators.ExerciseHistoryCacheInvalidator import (
    ExerciseHistoryCacheInvalidator,
)
from Backend.cache_proxies.key_formatters.ExerciseHistoryCacheKeyFormatter import (
    ExerciseHistoryCacheKeyFormatter,
)
from Backend.schemas.exercise_history import (
    ExerciseHistoryCachePrefixes,
    ExerciseHistoryCreate,
    ExerciseHistoryGetAll,
)
from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.tests.integration.conftest import TrDayData
from Backend.tests.integration.cache_proxy.conftest import keys_func
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestExerciseHistoryCacheProxy:

    @pytest.fixture
    def proxy(self, uow: UnitOfWork, redis: Redis):
        formatter = ExerciseHistoryCacheKeyFormatter()
        invalidator = ExerciseHistoryCacheInvalidator(redis, formatter)
        service = ExerciseHistoryService(uow)
        return ExerciseHistoryCacheProxy(service, redis, invalidator, formatter)

    @pytest.fixture
    def get_all_proxy_version_key(self, redis: Redis):
        async def _func():
            match = ExerciseHistoryCachePrefixes.version + ":*"

            return [key async for key in redis.scan_iter(match=match)]

        return _func

    async def test_create_create_new_version_for_get_all_key(
        self,
        proxy: ExerciseHistoryCacheProxy,
        tr_history_data: TrDayData,
        get_all_proxy_version_key: keys_func,
    ):
        user_id = tr_history_data.user_id
        training_day_history_id = tr_history_data.history.id

        data = ExerciseHistoryCreate(
            exercise_id=3, training_day_history_id=training_day_history_id
        )

        exercise_id = tr_history_data.history.exercises_history[0].exercise_id

        get_all_data = ExerciseHistoryGetAll(exercise_id=exercise_id, skip=0, limit=50)

        await proxy.get_all_exercise_history(user_id, get_all_data)

        assert len(await get_all_proxy_version_key()) == 0

        await proxy.create_exercise_history(user_id, data)

        assert len(await get_all_proxy_version_key()) > 0
