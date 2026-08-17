import pytest

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayApi:

    async def test_create_training_day(self, client, workout, user_authorized):
        request_body = {
            "name": "Chest",
            "day_order": 4
        }

        response = await client.post(f"/training_days/{workout.id}", json=request_body)

        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

    async def test_update_training_day(self, client, workout, user_authorized):
        request_body = {
            "name": "NewName"
        }
        
        day_id = workout.training_days[0].id

        response = await client.patch(f"/training_days/{workout.id}/{day_id}", json=request_body)

        assert response.status_code == 200
        assert request_body.items() <= response.json().items()

    async def test_delete_training_day(self, client, workout, user_authorized):
        day_id = workout.training_days[0].id
        response_delete = await client.delete(f"/training_days/{workout.id}/{day_id}")

        assert response_delete.status_code == 200
