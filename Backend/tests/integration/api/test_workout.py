import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutApi:

    async def test_create_workout(self, client, user_authorized):
        request_body = {
            "name": "TestWorkout",
            "description": "TestDescriptionHalo",
            "public": True
        }

        response = await client.post("/workouts/", json=request_body)

        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

       
    async def test_get_workout(self, client, workout, user_authorized):
        response = await client.get(f"/workouts/{workout.id}")
    
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_all_workouts(self, client, workout, user_authorized):
        response = await client.get("/workouts/get_all?my=True")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_update_workout(self, client, workout, user_authorized):
        request_body = {
            "name": "NewName",
            "description": "NewDescription"
        }
        
        response = await client.patch(f"/workouts/{workout.id}", json=request_body)
        response_json = response.json()
        assert response.status_code == 200
        assert request_body.items() <= response_json.items()

       
    async def test_delete_workout(self, client, user_authorized, workout):
        response_delete = await client.delete(f"/workouts/{workout.id}")

        assert response_delete.status_code == 200

        response_get = await client.get(f"/workouts/{workout.id}")

        assert response_get.status_code == 404
