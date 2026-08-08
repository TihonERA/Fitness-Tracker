import pytest

from Backend.models.workout import Workout
from Backend.repositories.DayExerciseRepository import DayExerciseRepository

@pytest.mark.asyncio(loop_scope="session")
class TestDayExerciseRepository:

    @pytest.fixture
    def repo(self, db_session):
        return DayExerciseRepository(session=db_session)

    async def test_delete_day_exercise(
        self,
        repo: DayExerciseRepository,
        workout: Workout
    ):
        day_id = workout.training_days[0].id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        fetched_day_exercise = await repo.get_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        assert fetched_day_exercise is not None

        await repo.delete_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        fetched_day_exercise = await repo.get_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        assert fetched_day_exercise is None
