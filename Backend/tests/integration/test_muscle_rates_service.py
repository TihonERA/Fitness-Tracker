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
        muscle_distribution_list = await service.get_muscle_distribution_list(
            workout.id
        )

        assert isinstance(muscle_distribution_list, dict)
        assert len(muscle_distribution_list) == 15

    async def test_get_muscle_antagonists_statuses(
        self, service: MuscleRatesService, workout: Workout
    ):
        muscle_antagonists_statuses = await service.get_muscle_antagonists_statuses(
            workout.id
        )

        assert isinstance(muscle_antagonists_statuses, list)
        assert len(muscle_antagonists_statuses) == 14
