import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutApi:

    @pytest.mark.parametrize("name, description, day_name", [ 
            ("1", "2", "3"),
            ("longname"*10, "longdesc"*40, "longdayname"*5)
    ])                
    async def test_create_workout_with_schedule(self, name, description, day_name, make_workout_factory_returning_data):
        workout_data = await make_workout_factory_returning_data(
            name=name, description=description, day_name=day_name
        )
        workout_data_json = workout_data.json()

        assert workout_data.status_code == 201
        assert len(workout_data_json["training_days"]) > 0
        assert len(workout_data_json["training_days"][0]["day_exercises"]) > 0 

    async def test_create_training_day(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        training_day_data = {
            "name": "Chest",
            "day_order": 4 
        }

        updated_workout = await client.post(f"/workouts/{old_workout_json["workout_id"]}/training_day", json=training_day_data)

        assert updated_workout.status_code == 200
        assert old_workout != updated_workout.json() 

    async def test_create_day_exercise(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()
        
        day_exercise_data = {
            "exercise_order": 2,
            "sets": 3,
            "reps": 15,
            "exercise_id": 2
        }

        workout_id = old_workout_json["workout_id"]
        training_day_id = old_workout_json["training_days"][0]["day_id"]
        updated_workout = await client.post(f"/workouts/{workout_id}/{training_day_id}/day_exercise", json=day_exercise_data)

        assert updated_workout.status_code == 200
        assert old_workout != updated_workout
        
    async def test_get_workout(self, client, make_workout_factory_returning_data):
        workout_data = await make_workout_factory_returning_data()
        workout_data_json = workout_data.json()

        response = await client.get(f"/workouts/{workout_data_json["workout_id"]}")
        response_json = response.json()

        assert response.status_code == 200
        assert len(response_json["training_days"]) > 0
        assert len(response_json["training_days"][0]["day_exercises"]) > 0

    async def test_get_all_workouts(self, client, make_workout_factory_returning_data):
        for i in range(1, 7):
            await make_workout_factory_returning_data(day_order=i)
        response = await client.get("/workouts/get_all?skip=1&limit=100&user_id=00000000-0000-0000-0000-000000000000&public=False")
        assert response.status_code == 200
        assert len(response.json()) > 1

    async def test_update_workout(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        workout_update_data = {
            "name": "NewName",
            "description": "NewDescription"
        }
        
        workout_id = old_workout_json["workout_id"]
        updated_workout = await client.patch(f"/workouts/{workout_id}", json=workout_update_data)
        updated_workout_json = updated_workout.json()

        assert updated_workout.status_code == 200
        assert updated_workout != old_workout
        assert updated_workout_json["name"] == workout_update_data["name"]
        assert updated_workout_json["description"] == workout_update_data["description"]

    async def test_update_training_day(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        training_day_update_data = {
            "name": "NewName"
        }

        workout_id = old_workout_json["workout_id"]
        training_day_id = old_workout_json["training_days"][0]["day_id"]
        updated_workout = await client.patch(f"/workouts/{workout_id}/training_day/{training_day_id}", json=training_day_update_data)
        updated_workout_json = updated_workout.json()

        assert updated_workout.status_code == 200
        assert updated_workout != old_workout
        assert updated_workout_json["training_days"][0]["name"] == training_day_update_data["name"]

    async def test_updated_day_exercise(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        day_exercise_update_data = {
            "sets": 2,
            "reps": 20
        } 

        workout_id = old_workout_json["workout_id"]
        training_day_id = old_workout_json["training_days"][0]["day_id"]
        exercise_id = old_workout_json["training_days"][0]["day_exercises"][0]["exercise_id"]
        updated_workout = await client.patch(f"/workouts/{workout_id}/{training_day_id}/day_exercise/{exercise_id}", json=day_exercise_update_data)
        updated_workout_json = updated_workout.json()

        assert updated_workout.status_code == 200
        assert old_workout != updated_workout_json
        assert updated_workout_json["training_days"][0]["day_exercises"][0]["sets"] == day_exercise_update_data["sets"]
        assert updated_workout_json["training_days"][0]["day_exercises"][0]["reps"] == day_exercise_update_data["reps"]
        
    async def test_delete_workout(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        workout_id = old_workout_json["workout_id"]
        await client.delete(f"/workouts/{workout_id}")

        deleted_workout = await client.get(f"/workouts/{workout_id}")

        assert deleted_workout.status_code == 404

    async def test_delete_training_day(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        workout_id = old_workout_json["workout_id"]
        training_day_id = old_workout_json["training_days"][0]["day_id"]
        
        await client.delete(f"/workouts/{workout_id}/{training_day_id}")

        deleted_training_day_in_workout = await client.get(f"/workouts/{workout_id}")
        deleted_training_day_in_workout_json = deleted_training_day_in_workout.json()

        assert deleted_training_day_in_workout_json["training_days"][0]["day_id"] != training_day_id

    async def test_delete_day_exercise(self, client, make_workout_factory_returning_data):
        old_workout = await make_workout_factory_returning_data()
        old_workout_json = old_workout.json()

        workout_id = old_workout_json["workout_id"]
        training_day_id = old_workout_json["training_days"][0]["day_id"]
        exercise_id = old_workout_json["training_days"][0]["day_exercises"][0]["exercise_id"]
        
        await client.delete(f"/workouts/{workout_id}/{training_day_id}/{exercise_id}")

        deleted_day_exercise_in_workout = await client.get(f"/workouts/{workout_id}")
        deleted_day_exercise_in_workout_json = deleted_day_exercise_in_workout.json()

        assert deleted_day_exercise_in_workout_json["training_days"][0]["day_exercises"][0]["exercise_id"] != exercise_id


    async def test_get_muscles_balance(self, client, make_workout_factory_returning_data):
        workout = await make_workout_factory_returning_data()
        workout_id = workout.json()["workout_id"]

        trigger_response = await client.post(f"/workouts/{workout_id}/muscles_balance_list")
        task_id = trigger_response.text.strip('"')
        print(task_id)

        for _ in range(10):
            status_response = await client.get(f"/tasks/{task_id}")
            status_data = status_response.json()
            
            if status_data["status"] == "SUCCESS":

                result = status_data["result"]
                
                assert result is not None
                assert isinstance(result, list)
                assert len(result) > 0
                return  
                
            elif status_data["status"] == "FAILURE":
                error_msg = status_data.get('result', 'Unknown error')

                print(f"\n❌ Ошибка: {error_msg}")
                print(f"❌ Задача {task_id} упала.")
                
                pytest.fail(f"Задача Celery упала с ошибкой: {error_msg}")
            await asyncio.sleep(1.0)
            
        pytest.fail("Воркер Celery не успел выполнить задачу")

    async def test_get_muscles_distribution_list(self, client, make_workout_factory_returning_data):
        workout = await make_workout_factory_returning_data()
        workout_id = workout.json()["workout_id"]

        trigger_response = await client.post(f"/workouts/{workout_id}/muscles_distribution_list")
        task_id = trigger_response.text.strip('"')
        print(task_id)

        for _ in range(10):
            status_response = await client.get(f"/tasks/{task_id}")
            status_data = status_response.json()
            
            if status_data["status"] == "SUCCESS":

                result = status_data["result"]
                
                assert result is not None
                assert isinstance(result, list)
                assert len(result) > 0
                return  
                
            elif status_data["status"] == "FAILURE":
                error_msg = status_data.get('result', 'Unknown error')

                print(f"\n❌ Ошибка: {error_msg}")
                print(f"❌ Задача {task_id} упала.")
                
                pytest.fail(f"Задача Celery упала с ошибкой: {error_msg}")
            await asyncio.sleep(1.0)
            
        pytest.fail("Воркер Celery не успел выполнить задачу")


      
