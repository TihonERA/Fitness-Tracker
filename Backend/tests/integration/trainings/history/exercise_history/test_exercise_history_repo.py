from datetime import datetime, timezone

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.repositories.ExerciseHistoryRepository import ExerciseHistoryRepository

from Backend.tests.integration.trainings.history.conftest import TrDayData

from Backend.schemas.exercise_history import ExerciseHistoryCreateDTO, SetsHistory

@pytest.mark.asyncio(loop_scope="session")
class TestExerciseHistoryRepository:

    @pytest.fixture
    def repo(self, db_session: AsyncSession):
        return ExerciseHistoryRepository(db_session)

    async def test_create(
        self,
        repo: ExerciseHistoryRepository,
        tr_history_data : TrDayData
    ):
        sets_history = SetsHistory(
            set=3,
            reps=10,
            weight=20.5,
            time_for_set=datetime.now()
        )
        data = ExerciseHistoryCreateDTO(
            user_id=tr_history_data.user_id,
            exercise_id=1,
            training_day_history_id=tr_history_data.history.id,
            sets_history=[sets_history]
        )

        created_history = await repo.create_exercise_history(data)

        assert len(created_history.sets_history) > 0
