from uuid import uuid4

from annotated_types import Ge
import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.use_cases.conftest import (
    CreateWorkout,
    create_workout,
)
from Backend.trainings.application.use_cases.workout.get_workout import (
    GetLoadedWorkoutUseCase,
)
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


@pytest.fixture
def use_case(repo: FakeWorkoutRepository) -> GetLoadedWorkoutUseCase:
    return GetLoadedWorkoutUseCase(repo)


async def test_success(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    fetched_workout = await use_case(workout.user_id, workout_id)

    assert fetched_workout is not None

    assert fetched_workout.id == workout_id


async def test_not_found(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    with pytest.raises(WorkoutNotFound):
        await use_case(user_id=uuid4(), workout_id=-1)


async def test_read_public(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    workout = await create_workout(public=True)
    workout_id = workout.id

    assert workout_id is not None

    fetched_workout = await use_case(user_id=uuid4(), workout_id=workout_id)

    assert fetched_workout is not None

    assert fetched_workout.id == workout_id


async def test_access_denied(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    with pytest.raises(WorkoutAccessDenied):
        await use_case(user_id=uuid4(), workout_id=workout_id)
