from uuid import uuid4

import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.use_cases.conftest import CreateWorkout
from Backend.tests.unit.trainings.workout_factories import WorkoutDTOFactory
from Backend.trainings.application.use_cases.workout.update_workout import (
    UpdateWorkoutUseCase,
)
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


@pytest.fixture
def use_case(repo: FakeWorkoutRepository) -> UpdateWorkoutUseCase:
    return UpdateWorkoutUseCase(repo)


async def test_success(
    workout_dto_factory: WorkoutDTOFactory,
    use_case: UpdateWorkoutUseCase,
    repo: FakeWorkoutRepository,
    create_workout: CreateWorkout,
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    command = workout_dto_factory.make_update_workout_command(
        user_id=workout.user_id,
        workout_id=workout_id,
        name="new_name",
        description="new_desc",
        public=True,
    )

    assert command.name is not None

    await use_case(command)

    workout = await repo.get(workout_id)

    assert workout is not None

    assert command.name.value == workout.name.value
    assert command.description == workout.description
    assert command.public == workout.public


async def test_not_found(
    workout_dto_factory: WorkoutDTOFactory, use_case: UpdateWorkoutUseCase
) -> None:
    command = workout_dto_factory.make_update_workout_command(
        user_id=uuid4(), workout_id=-1
    )

    with pytest.raises(WorkoutNotFound):
        await use_case(command)


async def test_access_denied(
    repo: FakeWorkoutRepository,
    workout_dto_factory: WorkoutDTOFactory,
    use_case: UpdateWorkoutUseCase,
    create_workout: CreateWorkout,
) -> None:
    workout = await create_workout()
    workout_id = workout.id

    assert workout_id is not None

    workout = await repo.get(workout_id)

    assert workout is not None

    command = workout_dto_factory.make_update_workout_command(
        user_id=uuid4(), workout_id=workout_id
    )

    with pytest.raises(WorkoutAccessDenied):
        await use_case(command)

    workout_after_update = await repo.get(workout_id)

    assert workout_after_update is not None

    assert workout.name.value == workout_after_update.name.value
    assert workout.description == workout_after_update.description
    assert workout.public == workout_after_update.public
