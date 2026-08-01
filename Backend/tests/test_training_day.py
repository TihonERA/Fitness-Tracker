import pytest

from Backend.api.v1 import day_exercise, workout

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayApi:

    async def test_get_training_day(self, client, make_workout, authorize):
        day_id = make_workout.training_days[0].day_id
        response = await client.get(f"/training_days/{make_workout.workout_id}/{day_id}")

        assert response.status_code == 200
        assert len(response.json()) > 0
        
    async def test_create_training_day(self, client, make_workout, authorize):
        request_body = {
            "name": "Chest",
            "day_order": 4
        }

        response = await client.post(f"/training_days/{make_workout.workout_id}", json=request_body)

        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

    async def test_update_training_day(self, client, make_workout, authorize):
        request_body = {
            "name": "NewName"
        }
        
        day_id = make_workout.training_days[0].day_id

        response = await client.patch(f"/training_days/{make_workout.workout_id}/{day_id}", json=request_body)

        assert response.status_code == 200
        assert request_body.items() <= response.json().items()

    async def test_delete_training_day(self, client, make_workout, authorize):
        day_id = make_workout.training_days[0].day_id
        response_delete = await client.delete(f"/training_days/{make_workout.workout_id}/{day_id}")

        assert response_delete.status_code == 200

        response_get = await client.get(f"/{make_workout.workout_id}/{day_id}")

        assert response_get.status_code == 404
