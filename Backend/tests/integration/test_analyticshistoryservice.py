import pytest

from Backend.tests.integration.conftest import TrDayData
from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.AnalyticsHistory import (
    CreateHistory,
    ExerciseDifference,
    ExerciseHistoryCreateNested,
    HistoryResponse,
    SetsDifference,
)
from Backend.schemas.exercise_history import ExerciseHistoryCreate, SetsHistory
from Backend.services.AnalyticsHistoryService import AnalyticsHistoryService
from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestAnalyticsHistoryService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        return AnalyticsHistoryService(uow)

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
                ExerciseHistoryCreateNested(
                    exercise_id=exercise_id,
                    sets_history=[SetsHistory(set=3, reps=10, weight=30)],
                )
            ],
        )

        history = await service.create_history(user_id=workout.user_id, data=data)

        assert isinstance(history, HistoryResponse)
        assert history.differences != []

        exercise = history.differences[0]
        assert isinstance(exercise, ExerciseDifference)

        set_difference = exercise.sets_differences[0]
        assert isinstance(set_difference, SetsDifference)

    async def test_create_history_without_exercises(
        self,
        service: AnalyticsHistoryService,
        workout: Workout,
        tr_history_data: TrDayData,
    ):
        day = workout.training_days[0]
        day_name = day.name
        day_id = day.id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        data = CreateHistory(day_name=day_name, day_id=day_id)

        history = await service.create_history(user_id=workout.user_id, data=data)

        assert history.differences == []

    async def test_create_history_without_last_history(
        self, service: AnalyticsHistoryService, workout: Workout
    ):
        day = workout.training_days[0]
        day_name = day.name
        day_id = day.id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        data = CreateHistory(
            day_name=day_name,
            day_id=day_id,
            exercises=[
                ExerciseHistoryCreateNested(
                    exercise_id=exercise_id,
                    sets_history=[SetsHistory(set=3, reps=10, weight=30)],
                )
            ],
        )

        history = await service.create_history(user_id=workout.user_id, data=data)

        assert history.last_training is None
        assert history.differences == []
