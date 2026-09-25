import pytest

from Backend.tests.unit.trainings.conftest import CreateWorkout
from Backend.tests.unit.trainings.training_day.conftest import CreateTrainingDay
from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.tests.unit.trainings.training_day.training_day_factories import (
    DayExerciseDTOFactory,
    TrainingDayDTOFactory,
)
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.application.use_cases.training_day.create_day_exercise import (
    CreateDayExerciseUseCase,
)


def use_case(
    access_service: TrainingDayAccessService, tr_day_repo: FakeTrainingDayRepository
) -> CreateDayExerciseUseCase:
    return CreateDayExerciseUseCase(access_service, tr_day_repo)


async def test_success(
    create_workout: CreateWorkout,
    create_training_day: CreateTrainingDay,
    day_exercises_dto_factory: DayExerciseDTOFactory,
) -> None:
    workout = await create_workout()

    assert workout.id is not None

    training_day = await create_training_day(workout_id=workout.id)

    assert training_day.id is not None

    command = day_exercises_dto_factory.make_create_day_exercise_command(
        user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
    )
