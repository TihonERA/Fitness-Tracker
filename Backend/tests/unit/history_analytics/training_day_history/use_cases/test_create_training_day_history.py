from Backend.history_analytics.application.use_cases.create_training_day_history import CreateTrainingDayHistoryUseCase
from Backend.history_analytics.application.dto.training_day_history import CreateTrainingDayHistoryCommand
import pytest

from Backend.tests.unit.history_analytics.training_day_history.fake_training_day_history_repository import FakeTrainingDayHistoryRepository

@pytest.fixture
def use_case(fake_tr_day_history_repo: FakeTrainingDayHistoryRepository) -> CreateTrainingDayHistoryUseCase:
    return CreateTrainingDayHistoryUseCase(fake_tr_day_history_repo)

async def test_create_success(use_case: CreateTrainingDayHistoryUseCase, fake_tr_day_history_repo: FakeTrainingDayHistoryRepository) -> None:
    UNBOUNDED = -1

    dto = CreateTrainingDayHistoryCommand(
        day_id=UNBOUNDED, day_name="name"
    )

    await use_case(dto)

    training_day_history = await




