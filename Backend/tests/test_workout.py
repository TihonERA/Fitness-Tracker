import pytest

@pytest.mark.asyncio(scope="session")
async def test_create_workout_with_schedule(client):
    data = {
        "user_id": "00000000-0000-0000-0000-000000000000",
        "name": "Split",
        "description": "TestDescription TestDescription TestDescription TestDescription TestDescription ",
        "training_days": [{
            "name": "Day1",
            "day_order": 1,
            "day_exercises": [{
                "exercise_id": 1,
                "exercise_order": 1,
                "sets": 4,
                "reps": 15
            }]
        }]
    }

    result = await client.post("/workout/workout_schedule", json=data)
    assert result.status_code == 201
        
@pytest.mark.asyncio(scope="session")
async def test_get_workout(client):
    response1 = await client.get("/workout/1")
    assert response1.status_code == 200
    
    response_invalid = await client.get("/workout/123")
    assert response_invalid.status_code == 404
    assert response_invalid.json()["detail"] == "Not Found"