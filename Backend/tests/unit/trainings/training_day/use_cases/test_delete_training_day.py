import pytest

from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.tests.unit.trainings.training_day.helpers import assert_same_tr_days
from Backend.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayFactory,
)
from Backend.tests.unit.trainings.workout_factories import WorkoutFactory
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.application.use_cases.training_day.delete_training_day import (
    DeleteTrainingDayUseCase,
)
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
)


@pytest.fixture
def use_case(
    access_service: TrainingDayAccessService, tr_day_repo: FakeTrainingDayRepository
) -> DeleteTrainingDayUseCase:
    return DeleteTrainingDayUseCase(access_service, tr_day_repo)


async def test_success(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    use_case: DeleteTrainingDayUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()

    assert workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    await use_case(
        user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
    )

    deleted_training_day = await tr_day_repo.get(training_day.id)

    assert deleted_training_day is None


async def test_atomicity(
    workout_factory: WorkoutFactory,
    tr_day_factory: TrainingDayFactory,
    use_case: DeleteTrainingDayUseCase,
    tr_day_repo: FakeTrainingDayRepository,
) -> None:
    workout = await workout_factory.create_workout()
    different_workout = await workout_factory.create_workout()

    assert workout.id is not None
    assert different_workout.id is not None

    training_day = await tr_day_factory.create_tr_day(workout_id=workout.id)

    assert training_day.id is not None

    with pytest.raises(TrainingDayAccessDenied):
        await use_case(
            user_id=different_workout.user_id,
            workout_id=different_workout.id,
            day_id=training_day.id,
        )

    fetched_training_day = await tr_day_repo.get(training_day.id)

    assert fetched_training_day is not None

    assert_same_tr_days(training_day, fetched_training_day)
