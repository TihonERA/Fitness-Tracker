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
)
from Backend.trainings.application.services.training_day_access_service import (
    TrainingDayAccessService,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.value_objects.day_order import DayOrder
from Backend.trainings.domain.value_objects.title import EntityTitle


@pytest.fixture
def tr_day_repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


CreateTrainingDay = Callable[..., Awaitable[TrainingDay]]


@pytest.fixture
def create_training_day(
    tr_day_repo: FakeTrainingDayRepository,
    faker: Faker,
) -> CreateTrainingDay:
    async def _create(
        workout_id: int, name: str | None = None, day_order: int | None = None
    ) -> TrainingDay:
        training_day = TrainingDay.create(
            workout_id=workout_id,
            name=EntityTitle(name if name is not None else faker.name()),
            day_order=DayOrder(day_order if day_order is not None else randint(1, 7)),
        )
        return await tr_day_repo.create(training_day)

    return _create


@pytest.fixture
def assert_same_tr_days() -> Callable:
    def _assert(tr_day1: TrainingDay, tr_day2: TrainingDay) -> None:
        assert tr_day1.id is not None
        assert tr_day2.id is not None

        assert tr_day1.id == tr_day2.id
        assert tr_day1.workout_id == tr_day2.workout_id
        assert tr_day1.name == tr_day2.name
        assert tr_day1.day_order == tr_day2.day_order

    return _assert


@pytest.fixture
def tr_day_dto_factory(faker: Faker) -> TrainingDayDTOFactory:
    return TrainingDayDTOFactory(faker)


@pytest.fixture
def access_service(
    workout_repo: FakeWorkoutRepository, tr_day_repo: FakeTrainingDayRepository
) -> TrainingDayAccessService:
    return TrainingDayAccessService(workout_repo, tr_day_repo)
