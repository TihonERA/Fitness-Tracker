import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.workout_factories import WorkoutDTOFactory
from Backend.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)
from Backend.trainings.domain.exceptions.workout_exceptions import TitleError


@pytest.fixture
def use_case(repo: FakeWorkoutRepository) -> CreateWorkoutUseCase:
    return CreateWorkoutUseCase(repo)


async def test_create_success(
    use_case: CreateWorkoutUseCase,
    workout_dto_factory: WorkoutDTOFactory,
    repo: FakeWorkoutRepository,
) -> None:
    command = workout_dto_factory.make_create_workout_command()

    workout = await use_case(command)

    assert workout.id is not None

    workout = await repo.get(workout.id)

    assert workout is not None

    assert command.name.value == workout.name.value
    assert command.description == workout.description
    assert command.public == workout.public
