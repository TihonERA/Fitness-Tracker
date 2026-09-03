import pytest

from Backend.tests.integration.conftest import TrDayData
from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.AnalyticsHistory import CreateHistory
from Backend.schemas.exercise_history import ExerciseHistoryCreate, SetsHistory
from Backend.services.AnalyticsHistoryService import AnalyticsHistoryService
from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestAnalyticsHistoryService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        ex_hist_service = ExerciseHistoryService(uow)
        tr_day_hist_service = TrainingDayHistoryService(uow)
        return AnalyticsHistoryService(uow, ex_hist_service, tr_day_hist_service)

    async def test_create_history(
        self,
        service: AnalyticsHistoryService,
        workout: Workout,
        tr_history_data: TrDayData,
    ):
        day = workout.training_days[0]
        day_name = day.name
        day_id = day.id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        data = CreateHistory(
            day_name=day.name,
            day_id=day_id,
            exercises=[
                ExerciseHistoryCreate(
                    exercise_id=exercise_id,
                    training_day_history_id=tr_history_data.history.id,
                    sets_history=[SetsHistory(set=3, reps=10, weight=30)],
                )
            ],
        )

        print(await service.create_history(user_id=workout.user_id, data=data))
