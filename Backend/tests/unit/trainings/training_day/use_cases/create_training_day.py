from typing import Awaitable, Callable

import pytest

from Backend.tests.unit.trainings.training_day.fake_training_day_repository import (
    FakeTrainingDayRepository,
)
from Backend.trainings.domain.training_day_model import TrainingDay


@pytest.fixture
def repo() -> FakeTrainingDayRepository:
    return FakeTrainingDayRepository()


CreateTrainingDay = Callable[..., Awaitable[TrainingDay]]


@pytest.fixture
def create_training_day(repo: FakeTrainingDayRepository) -> CreateTrainingDay:
    async def _create() -> TrainingDay:
        return TrainingDay.create()
