from uuid import UUID

import pytest

from Backend.models.workout import Workout
from Backend.schemas.day_exercise import DayExerciseCreateDTO
from Backend.services.DayExerciseService import DayExerciseService
from Backend.utils.uow import UnitOfWork

@pytest.mark.asyncio(loop_scope="session")
class TestDayExerciseService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        return DayExerciseService(uow=uow)

    async def test_create_day_exercise(
        self,
        service: DayExerciseService,
        workout: Workout
    ):
        day_id = workout.training_days[0].id
        data = DayExerciseCreateDTO(
            exercise_order=10,
            exercise_id=3,
            day_id=day_id
        )

        created_training_day = await service.create_day_exercise(
            user_id=workout.user_id,
            workout_id=workout.id,
            day_id=day_id,
            data=data
        )

        assert created_training_day.exercise_order == data.exercise_order
        assert created_training_day.exercise_id == data.exercise_id
        assert created_training_day.day_id == data.day_id

    async def test_delete_day_exercise(
        self,
        service: DayExerciseService,
        workout: Workout
    ):
        day_id = workout.training_days[0].id
        exercise_id = workout.training_days[0].day_exercises[0].exercise_id

        await service.delete_day_exercise(
            user_id=workout.user_id,
            workout_id=workout.id,
            day_id=day_id,
            exercise_id=exercise_id
        )
