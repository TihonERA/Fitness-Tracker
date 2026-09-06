from httpx import AsyncClient, delete
import pytest

from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.AnalyticsHistory import CreateHistory
from Backend.schemas.training_day_history import TrainingDayHistoryGetAll
from Backend.tests.integration.conftest import TrDayData, TrDayDatas


@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryAPI:

    async def test_get_tr_day_history(self, client, user_authorized, tr_history_data):
        history = tr_history_data.history
        history_id = history.id

        fetched_history = await client.get(f"/training_day_history/{history_id}")
        fetched_history = fetched_history.json()

        assert fetched_history["id"] == history_id

    async def test_get_all_tr_day_history(
        self, client: AsyncClient, user_authorized: User, tr_history_datas: TrDayDatas
    ):
        fetched_histories = await client.get(f"/training_day_history/all")

        assert len(fetched_histories.json()) > 1

    async def test_create_history(
        self, client: AsyncClient, user_authorized: User, workout: Workout
    ):
        day = workout.training_days[0]
        data = {"day_name": "Тренировка спины и бицепса", "day_id": 1, "exercises": []}

        stats = await client.post("/training_day_history/", json=data)
        new_history = stats.json()["new_training"]

        assert new_history["day_name"] == data["day_name"]
        assert new_history["day_id"] == data["day_id"]

    async def test_delete_history(
        self, client: AsyncClient, user_authorized: User, tr_history_data: TrDayData
    ):
        history_id = tr_history_data.history.id

        deleted_history = await client.delete(f"/training_day_history/{history_id}")

        assert deleted_history.status_code == 200

        fetched_history = await client.get(f"/training_day_history/{history_id}")

        assert fetched_history.status_code == 404
