from uuid import uuid4

import pytest

from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.utils.uow import UnitOfWork 

@pytest.fixture
def uow(mocker):
    mock_uow = mocker.AsyncMock(spec=UnitOfWork)

    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.workout = mocker.AsyncMock(spec=WorkoutRepository)
    mock_uow.trainingday = mocker.AsyncMock()
    mock_uow.dayexercise = mocker.AsyncMock()
    mock_uow.user = mocker.AsyncMock()
    mock_uow.trainingdayhistory = mocker.AsyncMock()

    return mock_uow

@pytest.fixture
def redis(mocker):
    return mocker.AsyncMock()

@pytest.fixture
def user_id():
    return uuid4()
