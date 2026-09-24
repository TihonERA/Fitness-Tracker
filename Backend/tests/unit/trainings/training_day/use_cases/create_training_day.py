from typing import Awaitable, Callable

from random import randint

from faker import Faker
import pytest

from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
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
    tr_day_repo: FakeTrainingDayRepository, faker: Faker
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
