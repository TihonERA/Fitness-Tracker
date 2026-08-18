import pytest

from Backend.schemas.training_day_history import TrainingDayHistoryGetAll
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.tests.integration.conftest import TrDayData

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryService:

    @pytest.fixture
    def service(self, uow):
        return TrainingDayHistoryService(uow)

    async def test_get_all_invalid(
        self,
        service: TrainingDayHistoryService,
        tr_day_history: TrDayData
    ):
        data = TrainingDayHistoryGetAll(
            skip=0,
            limit=50,
            user_id=tr_day_history.user_id,
            workout_id=-1
        )

        histories = await service.get_all_tr_day_history(data)

        assert histories == []


