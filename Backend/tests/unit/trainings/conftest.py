import pytest
from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository


@pytest.fixture
def workout_repo() -> FakeWorkoutRepository:
    return FakeWorkoutRepository()
