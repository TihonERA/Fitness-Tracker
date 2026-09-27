from typing import Awaitable, Callable
from uuid import uuid4

from faker import Faker
import pytest
from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.workout_factories import WorkoutFactory
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout


@pytest.fixture
def workout_repo() -> FakeWorkoutRepository:
    return FakeWorkoutRepository()


@pytest.fixture
def workout_factory(
    workout_repo: FakeWorkoutRepository, faker: Faker
) -> WorkoutFactory:
    return WorkoutFactory(workout_repo, faker)
