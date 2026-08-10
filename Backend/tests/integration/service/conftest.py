import pytest

from redis.asyncio import Redis

from Backend.utils.uow import UnitOfWork

from Backend.core.database import async_session_factory

from Backend.core.config import settings

@pytest.fixture
def uow(db_session):
    return UnitOfWork(session_maker=async_session_factory)

@pytest.fixture
def redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
