from typing import Awaitable, Callable
from uuid import uuid4

from faker import Faker
import pytest
from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.trainings.domain.value_objects.title import EntityTitle
from Backend.trainings.domain.workout_model import Workout


@pytest.fixture
def workout_repo() -> FakeWorkoutRepository:
    return FakeWorkoutRepository()


CreateWorkout = Callable[..., Awaitable[Workout]]


@pytest.fixture
def create_workout(workout_repo: FakeWorkoutRepository, faker: Faker) -> CreateWorkout:
    async def _create_func(
        name: str | None = None, description: str | None = None, public: bool = False
    ) -> Workout:
        workout = Workout.create(
            user_id=uuid4(),
            name=EntityTitle(name if name is not None else faker.name()),
            description=description,
            public=public,
        )

        return await workout_repo.create(workout)

    return _create_func
