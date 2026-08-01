import pytest

@pytest.mark.asyncio(loop_scope="session")
class TestDayExerciseAPI:

    async def test_get_day_exercise(self, client, make_workout, authorize_user):
        await authorize_user()

        day_id = make_workout.training_days[0].day_id
        exercise_id = make_workout.training_days[0].day_exercises[0].exercise_id

        response = await client.get(f"/day_exercises/{make_workout.workout_id}/{day_id}/{exercise_id}")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_create_day_exercise(self, client, make_workout, authorize_user):
        await authorize_user()

        day_id = make_workout.training_days[0].day_id

        request_body = {
            "exercise_order": 2,
            "sets": 3,
            "reps": 15,
            "exercise_id": 2
        }


        response = await client.post(f"/day_exercises/{make_workout.workout_id}/{day_id}", json=request_body)
    
        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

    async def test_update_day_exercise(self, client, make_workout, authorize_user):
        await authorize_user()

        day_id = make_workout.training_days[0].day_id
        exercise_id = make_workout.training_days[0].day_exercises[0].exercise_id

        request_body = {
            "sets": 2,
            "reps": 20
        } 
        
        response = await client.patch(f"/day_exercises/{make_workout.workout_id}/{day_id}/{exercise_id}", json=request_body)

        assert response.status_code == 200
        assert request_body.items() <= response.json().items()

    async def test_delete_day_exercise(self, client, make_workout, authorize_user):
        await authorize_user()

        day_id = make_workout.training_days[0].day_id
        exercise_id = make_workout.training_days[0].day_exercises[0].exercise_id


        response_delete = await client.delete(f"/day_exercises/{make_workout.workout_id}/{day_id}/{exercise_id}")

        assert response_delete.status_code == 200

        response_get = await client.get(f"/day_exercises/{make_workout.workout_id}/{day_id}/{exercise_id}")

        assert response_get.status_code == 404


