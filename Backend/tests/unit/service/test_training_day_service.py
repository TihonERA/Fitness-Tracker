from uuid import uuid4

import pytest

from unittest.mock import AsyncMock

from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.exceptions import Forbidden

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayService:

    @pytest.fixture
    def service(self, uow):
        return TrainingDayService(uow=uow)

    async def test_get_training_access(
        self,
        service: TrainingDayService
    ):
        workout = Workout(id=10, user_id=uuid4(), name="workout")
        service._get_instance_with_access = AsyncMock(return_value=workout)

        training_day = TrainingDay(id=1, workout_id=1, name="tr_day")
        service._get_existing_instance = AsyncMock(return_value=training_day)

        with pytest.raises(Forbidden):
            await service.get_training_day(
                user_id=workout.user_id,
                workout_id=workout.id,
                day_id=training_day.id
            )
