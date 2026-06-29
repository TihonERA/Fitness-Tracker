import pytest

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutApi:

    @pytest.mark.parametrize("name, description, day_name", [ 
            ("1", "2", "3"),
            ("longname"*10, "longdesc"*40, "longdayname"*5)
    ])                
    async def test_create_workout_with_schedule(self, client, name, description, day_name, make_workout_data):
        data = make_workout_data(name=name, description=description, day_name=day_name)
        result = await client.post("/workouts/workout_schedule", json=data)
        result_json = result.json()
        assert result.status_code == 201

        assert len(result_json["training_days"]) > 0
        assert len(result_json["training_days"][0]["day_exercises"]) > 0 

    async def test_get_workout(self, client, make_workout_data, db_session):
        data = make_workout_data()
        created_workout = await client.post("/workouts/workout_schedule", json=data)
        workout_json = created_workout.json()

        await db_session.commit()
        db_session.expire_all()

        response = await client.get(f"/workouts/{workout_json["workout_id"]}")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json["training_days"]) > 0
        assert len(response_json["training_days"][0]["day_exercises"]) > 0

    async def test_get_all_workouts(self, client, make_workout_data):
        for i in range(1, 7):
            await client.post("/workouts/workout_schedule", json=make_workout_data(day_order=i))
        response = await client.get("/workouts?skip=1&limit=100&user_id=00000000-0000-0000-0000-000000000000&public=False")
        assert response.status_code == 200
        assert len(response.json()) > 1
