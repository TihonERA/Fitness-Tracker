from faker import Faker
import pytest
from Backend.tests.unit.trainings.workout.workout_factories import WorkoutDTOFactory


@pytest.fixture
def workout_dto_factory(faker: Faker) -> WorkoutDTOFactory:
    return WorkoutDTOFactory(faker)
