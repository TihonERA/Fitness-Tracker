from uuid import UUID

from pydantic import BaseModel, ConfigDict
import pytest

from Backend.tests.integration.trainings.history.conftest import TrDayData, TrDayDatas

from Backend.models.exercise_history import ExerciseHistory
from Backend.models.training_day_history import TrainingDayHistory
from Backend.models.workout import Workout
from Backend.repositories.TrainingDayHistoryRepository import TrainingDayHistoryRepository
from Backend.schemas.training_day_history import TrainingDayHistoryGetAll

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryRepository:
    
    @pytest.fixture
    def service(self, db_session):
        return TrainingDayHistoryRepository(db_session)

    async def test_get(
        self,
        service: TrainingDayHistoryRepository,
        tr_day_history: TrDayData
    ):
        fetched_data = await service.get_tr_day_history(
            id=tr_day_history.history.id
        )

        assert fetched_data is not None
        assert len(fetched_data.exercises_history) > 0

    async def test_get_all(
        self, 
        service: TrainingDayHistoryRepository, 
        tr_day_histories: TrDayDatas
    ):
        data = TrainingDayHistoryGetAll(
            skip=0,
            limit=50,
            user_id=tr_day_histories.user_id, 
        )

        training_day_histories = await service.get_all_tr_day_history(data)
        assert len(training_day_histories) == len(tr_day_histories.histories)

    async def test_get_all_specific(
        self,
        service: TrainingDayHistoryRepository,
        tr_day_histories: TrDayDatas
    ):
        data = TrainingDayHistoryGetAll(
            skip=0,
            limit=50,
            user_id=tr_day_histories.user_id, 
            day_id=tr_day_histories.histories[0].day_id
        )
        training_day_histories = await service.get_all_tr_day_history(data)

        assert len(training_day_histories) == 1
