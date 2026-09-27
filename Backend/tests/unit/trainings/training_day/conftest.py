from random import randint
from typing import Awaitable, Callable

from faker import Faker
import pytest

from Backend.tests.unit.trainings.fake_workout_repository import FakeWorkoutRepository
from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.tests.unit.trainings.training_day.training_day_factories import (
    TrainingDayDTOFactory,
    TrainingDayFactory,
)
from Backend.tests.unit.trainings.workout_factories import WorkoutFactory
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


@pytest.fixture
def tr_day_repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


@pytest.fixture
def tr_day_factory(
    tr_day_repo: FakeTrainingDayRepository,
    faker: Faker,
) -> TrainingDayFactory:
    return TrainingDayFactory(tr_day_repo, faker)


@pytest.fixture
def tr_day_dto_factory(faker: Faker) -> TrainingDayDTOFactory:
    return TrainingDayDTOFactory(faker)


@pytest.fixture
def access_service(
    workout_repo: FakeWorkoutRepository, tr_day_repo: FakeTrainingDayRepository
) -> TrainingDayAccessService:
    return TrainingDayAccessService(workout_repo, tr_day_repo)
