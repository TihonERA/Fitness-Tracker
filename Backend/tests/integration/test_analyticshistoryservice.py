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
from Backend.schemas.exercise_history import ExerciseHistoryCreate, SetsHistoryCreate
from Backend.services.AnalyticsHistoryService import AnalyticsHistoryService
from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.utils.uow import UnitOfWork


@pytest.mark.asyncio(loop_scope="session")
class TestAnalyticsHistoryService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        tr_day_history_service = TrainingDayHistoryService(uow)
        ex_history_service = ExerciseHistoryService(uow)
        return AnalyticsHistoryService(tr_day_history_service, ex_history_service)

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
                    sets_history=[SetsHistoryCreate(set=3, reps=10, weight=30)],
                )
            ],
        )

        history = await service.create_history(user_id=workout.user_id, data=data)

        assert history["differences"] != []

        exercises = history["differences"]
        assert isinstance(exercises, list)

        exercise = exercises[0]
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

        exercise_differences = history["differences"]
        assert isinstance(exercise_differences, list)

        exercise_difference = exercise_differences[0]
        assert isinstance(exercise_difference, ExerciseDifference)
        assert exercise_difference.exercise_id is None
        assert exercise_difference.sets_differences == []

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
                    sets_history=[SetsHistoryCreate(set=3, reps=10, weight=30)],
                )
            ],
        )

        history = await service.create_history(user_id=workout.user_id, data=data)

        assert history.get("last_training") is None
        assert history.get("differences") == []

    async def test_create_history_less_sets_then_previous_training(
        self, service: AnalyticsHistoryService, workout: Workout
    ):
        user_id = workout.user_id
        day = workout.training_days[0]
        day_name = day.name
        day_id = day.id
        exercises = day.day_exercises

        data_last = CreateHistory(
            day_name=day_name,
            day_id=day_id,
            exercises=[
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[0].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=10, weight=20),
                        SetsHistoryCreate(set=2, reps=10, weight=20),
                        SetsHistoryCreate(set=3, reps=10, weight=20),
                    ],
                ),
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[1].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=10, weight=20),
                        SetsHistoryCreate(set=2, reps=10, weight=20),
                        SetsHistoryCreate(set=3, reps=10, weight=20),
                    ],
                ),
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[2].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=10, weight=20),
                        SetsHistoryCreate(set=2, reps=10, weight=20),
                        SetsHistoryCreate(set=3, reps=10, weight=20),
                    ],
                ),
            ],
        )

        last_history = await service.create_history(user_id=user_id, data=data_last)

        data_new = CreateHistory(
            day_name=day_name,
            day_id=day_id,
            exercises=[
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[0].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=15, weight=20),
                        SetsHistoryCreate(set=2, reps=15, weight=20),
                        SetsHistoryCreate(set=3, reps=15, weight=20),
                    ],
                ),
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[1].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=15, weight=20),
                        SetsHistoryCreate(set=2, reps=15, weight=20),
                        SetsHistoryCreate(set=3, reps=15, weight=20),
                    ],
                ),
                ExerciseHistoryCreateNested(
                    exercise_id=exercises[2].exercise_id,
                    sets_history=[
                        SetsHistoryCreate(set=1, reps=15, weight=20),
                    ],
                ),
            ],
        )

        new_history = await service.create_history(user_id=user_id, data=data_new)
