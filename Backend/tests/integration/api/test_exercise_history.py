from httpx import AsyncClient
import pytest
from redis.asyncio import Redis

from Backend.cache_proxies.ExerciseHistoryCacheProxy import ExerciseHistoryCacheProxy
from Backend.cache_proxies.invalidators.ExerciseHistoryCacheInvalidator import (
    ExerciseHistoryCacheInvalidator,
)
from Backend.cache_proxies.key_formatters.ExerciseHistoryCacheKeyFormatter import (
    ExerciseHistoryCacheKeyFormatter,
)
from Backend.models.user import User
from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.tests.integration.conftest import TrDayData
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestExerciseHistoryAPI:

    async def test_get_all_exercise_history(
        self,
        client: AsyncClient,
        user_authorized: User,
        tr_history_data: TrDayData,
    ):
        exercise_id = tr_history_data.history.exercises_history[0].exercise_id

        fetched_histories = await client.get(
            "/exercise_history/all", params={"exercise_id": exercise_id}
        )

        print(fetched_histories.json())
        assert fetched_histories.status_code == 200
        assert len(fetched_histories.json()) > 0

    async def test_get_exercise_history(
        self, client: AsyncClient, user_authorized: User, tr_history_data: TrDayData
    ):
        history_id = tr_history_data.history.exercises_history[0].id

        fetched_history = await client.get(f"/exercise_history/{history_id}")

        assert fetched_history.status_code == 200

    async def test_create_exercise_history(
        self, client: AsyncClient, user_authorized: User, tr_history_data: TrDayData
    ):
        exercise_id = tr_history_data.history.exercises_history[0].exercise_id
        training_day_history_id = tr_history_data.history.id

        data = {
            "exercise_id": exercise_id,
            "training_day_history_id": training_day_history_id,
        }

        created_history = await client.post("/exercise_history/", json=data)

        assert created_history.status_code == 200

    async def test_delete_history(
        self, client: AsyncClient, user_authorized: User, tr_history_data: TrDayData
    ):
        history_id = tr_history_data.history.exercises_history[0].id

        deleted_history = await client.delete(f"/exercise_history/{history_id}")

        assert deleted_history.status_code == 200
