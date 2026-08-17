import pytest

from Backend.models.workout import Workout

@pytest.mark.asyncio(loop_scope="session")
class TestDayExerciseAPI:

    async def test_create_day_exercise(self, client, workout, user_authorized):
        day_id = workout.training_days[0].id

        request_body = {
            "exercise_order": 2,
            "exercise_id": 2
        }


        response = await client.post(f"/day_exercises/{workout.id}/{day_id}", json=request_body)
    
        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

    # async def test_update_day_exercise(self, client, workout, user_authorized):
    #     day_id = workout.training_days[0].id
    #     exercise_id = workout.training_days[0].day_exercises[0].exercise_id
    #
    #     request_body = {
    #         "sets": 2,
    #         "reps": 20
    #     } 
    #
    #     response = await client.patch(f"/day_exercises/{workout.id}/{day_id}/{exercise_id}", json=request_body)
    #
    #     assert response.status_code == 200
    #     assert request_body.items() <= response.json().items()

    async def test_delete_day_exercise(self, client, workout, user_authorized):
        day_id = workout.training_days[0].id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id


        response_delete = await client.delete(f"/day_exercises/{workout.id}/{day_id}/{exercise_id}")

        assert response_delete.status_code == 200
