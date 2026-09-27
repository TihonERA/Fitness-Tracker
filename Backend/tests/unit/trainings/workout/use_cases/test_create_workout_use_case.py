import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.workout_factories import WorkoutDTOFactory
from Backend.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)


@pytest.fixture
def use_case(workout_repo: FakeWorkoutRepository) -> CreateWorkoutUseCase:
    return CreateWorkoutUseCase(workout_repo)


async def test_create_success(
    use_case: CreateWorkoutUseCase,
    workout_dto_factory: WorkoutDTOFactory,
    workout_repo: FakeWorkoutRepository,
) -> None:
    command = workout_dto_factory.make_create_workout_command()

    workout = await use_case(command)

    assert workout.id is not None

    workout = await workout_repo.get(workout.id)

    assert workout is not None

    assert command.name == workout.name.value
    assert command.description == workout.description
    assert command.public == workout.public
