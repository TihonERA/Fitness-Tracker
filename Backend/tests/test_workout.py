import pytest

def test_create_workout_with_schedule(client):
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

    result = client.post("/workout/workout_schedule", json=data)
    assert result.status_code == 201
        
