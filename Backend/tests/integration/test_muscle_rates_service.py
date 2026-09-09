import pytest

from Backend.models.workout import Workout
from Backend.utils.uow import UnitOfWork
from Backend.services.MuscleRatesService import MuscleRatesService


@pytest.mark.asyncio(loop_scope="session")
class TestMuscleRatesService:

    @pytest.fixture
    def service(self, uow: UnitOfWork) -> MuscleRatesService:
        return MuscleRatesService(uow)

    async def test_get_muscle_distribution_list(
        self, service: MuscleRatesService, workout: Workout
    ):
        user_id = workout.user_id

        muscle_distribution_list = await service.get_muscle_distribution_list(
            user_id, workout.id
        )

        assert isinstance(muscle_distribution_list, dict)
