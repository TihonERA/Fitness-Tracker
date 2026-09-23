from uuid import uuid4

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
from Backend.trainings.domain.workout_model import Workout


@pytest.fixture
def use_case(repo: FakeWorkoutRepository) -> GetLoadedWorkoutUseCase:
    return GetLoadedWorkoutUseCase(repo)


def _assert_same_workouts(first_workout: Workout, second_workout: Workout) -> bool:
    assert first_workout.id == second_workout.id
    assert first_workout.user_id == second_workout.user_id
    assert first_workout.name.value == second_workout.name.value
    assert first_workout.description == second_workout.description
    assert first_workout.public == second_workout.public

    return True


async def test_success(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    fetched_workout = await use_case(workout.user_id, workout_id)

    assert fetched_workout is not None

    assert _assert_same_workouts(workout, fetched_workout)


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

    assert _assert_same_workouts(workout, fetched_workout)


async def test_access_denied(
    create_workout: CreateWorkout, use_case: GetLoadedWorkoutUseCase
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    with pytest.raises(WorkoutAccessDenied):
        await use_case(user_id=uuid4(), workout_id=workout_id)
