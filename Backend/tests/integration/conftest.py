import asyncio
from dataclasses import dataclass
import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import Table, select, text
from sqlalchemy.dialects.postgresql import insert
import uuid
from Backend.models.base import Base
from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.models.trainingday import TrainingDay
from Backend.models.dayexercise import DayExercise
from Backend.models.training_day_history import TrainingDayHistory
from Backend.models.exercise_history import ExerciseHistory
from Backend.core.database import async_session_factory, async_engine
from Backend.core.config import settings
from alembic.config import Config
from alembic import command
from pathlib import Path

import random

from faker import Faker

from typing import cast

from Backend.services.UserService import UserService
from Backend.services.WorkoutService import WorkoutService
from Backend.utils.uow import UnitOfWork

alembic_ini_path = Path(__file__).parent.parent.parent.parent / "alembic.ini"

@pytest.fixture(scope="function")
async def db_session():
    async with async_session_factory() as session:
        yield session
        
        await session.rollback()

@pytest.fixture(scope="session")
async def setup_migrations():
    alembic_cfg = Config(str(alembic_ini_path))
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")


@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown_database():
    async with async_engine.begin() as conn:
        await conn.execute(text(
            'TRUNCATE TABLE "user", workout, trainingday, dayexercise, '
            'trainingdayhistory, exercisehistory RESTART IDENTITY CASCADE;'
        ))
        
    yield  
    
    async with async_engine.begin() as conn:
        await conn.execute(text(
            'TRUNCATE TABLE "user", workout, trainingday, dayexercise, '
            'trainingdayhistory, exercisehistory RESTART IDENTITY CASCADE;'
        ))

@pytest.fixture(scope="function", autouse=True)
async def clear_redis():
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    await redis.flushall()

    await redis.aclose()

@pytest.fixture
async def user(db_session):
    user = User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        email="testuser@mail.com",
        login="testuserlogin",
        hash_password="$argon2id$v=19$m=65536,t=3,p=4$b04HUqHrntSERdQIO+Nz0A$hmNV+lnF9Y6t46tCnXfBJEIxH4MEZZuE69h8RCjBmhA"
    )
    db_session.add(user)
    await db_session.commit()

    yield user

@pytest.fixture
def uow(db_session):
    return UnitOfWork(session_maker=async_session_factory)

@pytest.fixture
def redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
