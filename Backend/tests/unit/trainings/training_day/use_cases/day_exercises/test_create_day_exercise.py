import pytest

from Backend.tests.unit.trainings.training_day.conftest import (
    tr_day_repo,
)
from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.tests.unit.trainings.training_day.helpers import assert_same_tr_days
from Backend.tests.unit.trainings.training_day.training_day_factories import (
    DayExerciseDTOFactory,
    TrainingDayDTOFactory,
    TrainingDayFactory,
)
from Backend.tests.unit.trainings.workout_factories import WorkoutFactory
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.application.use_cases.training_day.create_day_exercise import (
    CreateDayExerciseUseCase,
)
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
)
from Backend.trainings.domain.training_day_model import TrainingDay


@pytest.fixture
def use_case(
    access_service: TrainingDayAccessService, tr_day_repo: FakeTrainingDayRepository
) -> CreateDayExerciseUseCase:
    return CreateDayExerciseUseCase(access_service, tr_day_repo)


async def test_success(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    day_exercises_dto_factory: DayExerciseDTOFactory,
    use_case: CreateDayExerciseUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.day_exercises == []
    assert training_day.id is not None

    command = day_exercises_dto_factory.make_create_day_exercise_command(
        user_id=workout.user_id,
        workout_id=training_day.workout_id,
        day_id=training_day.id,
    )

    await use_case(command)

    training_day_after_update = await tr_day_repo.get(training_day.id)

    assert training_day_after_update is not None
    assert len(training_day_after_update.day_exercises) == 1

    day_exercise = training_day_after_update.day_exercises[0]

    assert_same_tr_days(training_day, training_day_after_update)
    assert day_exercise.day_id == command.day_id
    assert day_exercise.exercise_id == command.exercise_id
    assert day_exercise.exercise_order.value == command.exercise_order


async def test_atomicity(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    day_exercises_dto_factory: DayExerciseDTOFactory,
    use_case: CreateDayExerciseUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()
    different_workout = await workout_factory.create_workout()

    assert workout.id is not None
    assert different_workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    command = day_exercises_dto_factory.make_create_day_exercise_command(
        user_id=different_workout.user_id,
        workout_id=different_workout.id,
        day_id=training_day.id,
    )

    with pytest.raises(TrainingDayAccessDenied):
        await use_case(command)

    training_day_after_update = await tr_day_repo.get(training_day.id)

    assert training_day_after_update is not None

    assert_same_tr_days(training_day, training_day_after_update)
    assert training_day.day_exercises == training_day_after_update.day_exercises
