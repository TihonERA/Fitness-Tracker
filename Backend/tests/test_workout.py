import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutApi:

    async def test_create_workout(self, client, authorize_user):
        await authorize_user()
        request_body = {
            "name": "TestWorkout",
            "description": "TestDescriptionHalo",
            "public": True
        }

        response = await client.post("/workouts/", json=request_body)

        assert response.status_code == 201
        assert request_body.items() <= response.json().items()

       
    async def test_get_workout(self, client, make_workout, authorize_user):
        await authorize_user()
        response = await client.get(f"/workouts/{make_workout.workout_id}")
    
        print(make_workout.workout_id, make_workout.user_id, response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_all_workouts(self, client, make_workout, authorize_user):
        await authorize_user() 

        response = await client.get("/workouts/get_all?my=True")
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_update_workout(self, client, make_workout, authorize_user):
        await authorize_user()

        request_body = {
            "name": "NewName",
            "description": "NewDescription"
        }
        
        response = await client.patch(f"/workouts/{make_workout.workout_id}", json=request_body)
        response_json = response.json()

        assert response.status_code == 200
        assert request_body.items() <= response_json.items()

       
    async def test_delete_workout(self, client, authorize_user, make_workout):
        await authorize_user()

        response_delete = await client.delete(f"/workouts/{make_workout.workout_id}")

        assert response_delete.status_code == 200

        response_get = await client.get(f"/workouts/{make_workout.workout_id}")

        assert response_get.status_code == 404

    async def test_get_muscles_balance(self, client, make_workout):
        workout_id = make_workout.workout_id

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

    async def test_get_muscles_distribution_list(self, client, make_workout):
        workout_id = make_workout.workout_id

        trigger_response = await client.post(f"/workouts/{workout_id}/muscles_distribution_list")
        task_id = trigger_response.text.strip('"')

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


      
