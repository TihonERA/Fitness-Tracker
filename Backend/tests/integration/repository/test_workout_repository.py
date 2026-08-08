import random
from typing import Sequence
import uuid

import pytest

from Backend.models.workout import Workout
from Backend.repositories.WorkoutRepository import WorkoutRepository

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutRepository:
    
    @pytest.fixture
    def repo(self, db_session):
        return WorkoutRepository(session=db_session)

    async def test_get_workout(self, repo, workout):
        fetched_workout = await repo.get_workout(workout_id=workout.id)

        random_training_day_index = random.randint(1,3)

        assert workout == fetched_workout
        assert len(fetched_workout.training_days) > 0
        assert len(fetched_workout.training_days[0].day_exercises) > 0
    
    async def test_get_workout_invalid(self, repo, workout):
        fetched_workout = await repo.get_workout(workout_id=-1)

        assert fetched_workout is None

    async def test_get_workout_and_check_access(self, repo: WorkoutRepository, workout):
        fetched_workout = await repo.get_workout_and_check_access(
            user_id=workout.user_id, 
            workout_id=workout.id
        )

        assert fetched_workout is not None
        assert fetched_workout == workout

    async def test_get_workout_and_check_access_invalid(
        self, 
        repo: WorkoutRepository, 
        workout: Workout
    ):
        fake_user_id = uuid.uuid4()

        fetched_workout = await repo.get_workout_and_check_access(
            user_id=fake_user_id,
            workout_id=workout.id
        )

        assert fetched_workout is None

    async def test_get_all_workouts(
        self,
        repo: WorkoutRepository,
        workout: Workout
    ):
        fetched_workouts = await repo.get_all_workouts(skip=0, limit=50)

        assert isinstance(fetched_workouts, list)
        assert workout.id in fetched_workouts
