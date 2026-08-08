import pytest

from Backend.models.workout import Workout
from Backend.repositories.TrainingDayRepository import TrainingDayRepository

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayRepository:

    @pytest.fixture
    def repo(self, db_session):
        return TrainingDayRepository(session=db_session)

    async def test_get_loaded_training_day(
        self,
        repo: TrainingDayRepository,
        workout: Workout
    ):
        day = workout.training_days[0]
        fetched_training_day = await repo.get_loaded_training_day(
            day_id=day.id
        )

        assert fetched_training_day == day
