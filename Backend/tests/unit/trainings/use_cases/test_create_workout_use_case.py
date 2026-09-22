import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.workout_fabrics import WorkoutDTOFactory
from Backend.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)
from Backend.trainings.domain.exceptions.workout_exceptions import TitleError


@pytest.fixture
def repo() -> FakeWorkoutRepository:
    return FakeWorkoutRepository()


@pytest.fixture
def workout_dto_fabric() -> WorkoutDTOFactory:
    return WorkoutDTOFactory()


@pytest.fixture
def use_case(repo: FakeWorkoutRepository) -> CreateWorkoutUseCase:
    return CreateWorkoutUseCase(repo)


async def test_create_success(
    use_case: CreateWorkoutUseCase,
    workout_dto_fabric: WorkoutDTOFactory,
    repo: FakeWorkoutRepository,
) -> None:
    command = workout_dto_fabric.make_create_workout_command()

    workout = await use_case(command)

    assert isinstance(workout.id, int)
    assert await repo.get(workout.id) == workout
