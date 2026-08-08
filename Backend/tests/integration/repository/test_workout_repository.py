import pytest

from Backend.repositories.WorkoutRepository import WorkoutRepository

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutRepository:
    
    @pytest.fixture
    def repo(self, db_session):
        return WorkoutRepository(session=db_session)

    async def test_get_workout(self, db_session, repo, workout):
        workout = await repo.get_workout(id=workout.id)

        assert workout is not None 
