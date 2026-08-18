from uuid import UUID

from pydantic import BaseModel, ConfigDict
import pytest

from Backend.models.exercise_history import ExerciseHistory
from Backend.models.training_day_history import TrainingDayHistory
from Backend.models.workout import Workout
from Backend.repositories.TrainingDayHistory import TrainingDayHistoryRepository

class TrDayData(BaseModel):
    user_id: UUID
    workout_id: int
    histories: list[TrainingDayHistory]

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryRepository:
    
    @pytest.fixture
    def service(self, db_session):
        return TrainingDayHistoryRepository(db_session)

    @pytest.fixture
    async def tr_day_history(self, workout: Workout, db_session):
        days = [
            workout.training_days[0],
            workout.training_days[1],
            workout.training_days[2]
        ]
        histories = []
        for day in days:
            history = TrainingDayHistory(
                day_id=day.id,
                day_name=day.name
            )
            histories.append(history)
            db_session.add(history)

        await db_session.flush()

        exercise_history = ExerciseHistory(
            user_id=workout.user_id,
            exercise_id=workout.training_days[0].day_exercises[0].exercise_id,
            training_day_history_id=histories[0].id,
            weight=10.0,
            sets=3,
            reps=10
        )
        db_session.add(exercise_history)

        await db_session.flush()

        data = TrDayData(
            user_id=workout.user_id,
            workout_id=workout.id,
            histories=histories
        )
        return data

    async def test_get(
        self,
        service: TrainingDayHistoryRepository,
        tr_day_history: TrDayData
    ):
        fetched_data = await service.get_tr_day_history(
            id=tr_day_history.histories[0].id
        )

        assert fetched_data is not None
        assert len(fetched_data.exercises_history) > 0

    async def test_get_all(
        self, 
        service: TrainingDayHistoryRepository, 
        tr_day_history: TrDayData
    ):
        training_day_histories = await service.get_all_tr_day_history(tr_day_history.user_id)
        assert len(training_day_histories) == len(tr_day_history.histories)

    async def test_get_all_specific(
        self,
        service: TrainingDayHistoryRepository,
        tr_day_history: TrDayData
    ):
        training_day_histories = await service.get_all_tr_day_history(
            user_id=tr_day_history.user_id,
            day_id=tr_day_history.histories[0].day_id
        )

        assert len(training_day_histories) == 1
