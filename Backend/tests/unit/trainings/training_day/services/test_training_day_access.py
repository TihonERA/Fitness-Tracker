from typing import Callable
from uuid import uuid4

import pytest

from Backend.tests.unit.trainings.conftest import CreateWorkout
from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.training_day.conftest import CreateTrainingDay
from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.trainings.application.dto import training_day
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayAccessDenied,
    TrainingDayNotFound,
)
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


@pytest.fixture
def service(
    workout_repo: FakeWorkoutRepository, tr_day_repo: FakeTrainingDayRepository
) -> TrainingDayAccessService:
    return TrainingDayAccessService(workout_repo, tr_day_repo)


async def test_success(
    create_workout: CreateWorkout,
    create_training_day: CreateTrainingDay,
    service: TrainingDayAccessService,
    assert_same_tr_days: Callable,
) -> None:
    workout = await create_workout()

    assert workout.id is not None

    training_day = await create_training_day(workout_id=workout.id)

    assert training_day.id is not None

    fetched_training_day = await service.get_authorized_day(
        user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
    )

    assert_same_tr_days(training_day, fetched_training_day)


async def test_workout_not_found(
    create_workout: CreateWorkout,
    create_training_day: CreateTrainingDay,
    service: TrainingDayAccessService,
) -> None:
    training_day = await create_training_day(workout_id=0)

    assert training_day.id is not None

    with pytest.raises(WorkoutNotFound):
        await service.get_authorized_day(
            user_id=uuid4(), workout_id=-1, day_id=training_day.id
        )


async def test_workout_access_denied(
    create_workout: CreateWorkout,
    create_training_day: CreateTrainingDay,
    service: TrainingDayAccessService,
) -> None:
    workout = await create_workout()

    assert workout.id is not None

    training_day = await create_training_day(workout_id=workout.id)

    assert training_day.id is not None

    with pytest.raises(WorkoutAccessDenied):
        await service.get_authorized_day(
            user_id=uuid4(), workout_id=workout.id, day_id=training_day.id
        )


async def test_tr_day_not_found(
    create_workout: CreateWorkout, service: TrainingDayAccessService
) -> None:
    workout = await create_workout()

    assert workout.id is not None

    with pytest.raises(TrainingDayNotFound):
        await service.get_authorized_day(
            user_id=workout.user_id, workout_id=workout.id, day_id=-1
        )


async def test_tr_day_access_denied(
    create_workout: CreateWorkout,
    create_training_day: CreateTrainingDay,
    service: TrainingDayAccessService,
) -> None:
    workout = await create_workout()

    assert workout.id is not None

    training_day = await create_training_day(workout_id=-1)

    assert training_day.id is not None

    with pytest.raises(TrainingDayAccessDenied):
        await service.get_authorized_day(
            user_id=workout.user_id, workout_id=workout.id, day_id=training_day.id
        )
