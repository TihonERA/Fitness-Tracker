import pytest

from Backend.models.workout import Workout
from Backend.schemas.training_day_history import TrainingDayHistoryCreate, TrainingDayHistoryGetAll
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.tests.integration.trainings.history.conftest import TrDayData
from Backend.utils.exceptions import NotFound

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryService:

    @pytest.fixture
    def service(self, uow):
        return TrainingDayHistoryService(uow)

    async def test_create(self, service: TrainingDayHistoryService, workout: Workout):
        data = TrainingDayHistoryCreate(
            day_name=workout.training_days[0].name,
            day_id=workout.training_days[0].id
        )

        history = await service.create_history(data)

        assert history.day_name == data.day_name
        assert history.day_id == data.day_id

    async def test_get_all_invalid(
        self,
        service: TrainingDayHistoryService,
        tr_history_data: TrDayData
    ):
        data = TrainingDayHistoryGetAll(
            skip=0,
            limit=50,
            user_id=tr_history_data.user_id,
            workout_id=-1
        )

        histories = await service.get_all_tr_day_history(data)

        assert histories == []


    async def test_delete(
        self,
        service: TrainingDayHistoryService,
        tr_history_data: TrDayData
    ):
        history_id = tr_history_data.history.id

        await service.delete_history(history_id)

        with pytest.raises(NotFound):
            await service.get_loaded_tr_day_history(history_id)
