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
async def workout(db_session: AsyncSession, user):
    day_1 = TrainingDay(name="Тренировка спины и бицепса", day_order=1)
    day_2 = TrainingDay(name="Тренировка груди, плеч и трицепса", day_order=2)
    day_3 = TrainingDay(name="Тренировка ног и пресса", day_order=3)

    ex_1_1 = DayExercise(exercise_id=9, exercise_order=1, training_day=day_1)
    ex_1_2 = DayExercise(exercise_id=10, exercise_order=2, training_day=day_1)
    ex_1_3 = DayExercise(exercise_id=11, exercise_order=3, training_day=day_1)
    ex_1_4 = DayExercise(exercise_id=18, exercise_order=4, training_day=day_1)
    ex_1_5 = DayExercise(exercise_id=29, exercise_order=5, training_day=day_1)
    ex_1_6 = DayExercise(exercise_id=43, exercise_order=6, training_day=day_1)

    ex_2_1 = DayExercise(exercise_id=3, exercise_order=1, training_day=day_2)
    ex_2_2 = DayExercise(exercise_id=5, exercise_order=2, training_day=day_2)
    ex_2_3 = DayExercise(exercise_id=21, exercise_order=3, training_day=day_2)
    ex_2_4 = DayExercise(exercise_id=22, exercise_order=4, training_day=day_2)
    ex_2_5 = DayExercise(exercise_id=37, exercise_order=5, training_day=day_2)
    ex_2_6 = DayExercise(exercise_id=45, exercise_order=6, training_day=day_2)

    ex_3_1 = DayExercise(exercise_id=47, exercise_order=1, training_day=day_3)
    ex_3_2 = DayExercise(exercise_id=17, exercise_order=2, training_day=day_3)
    ex_3_3 = DayExercise(exercise_id=52, exercise_order=3, training_day=day_3)
    ex_3_4 = DayExercise(exercise_id=59, exercise_order=4, training_day=day_3)
    ex_3_5 = DayExercise(exercise_id=42, exercise_order=5, training_day=day_3)
    ex_3_6 = DayExercise(exercise_id=40, exercise_order=6, training_day=day_3)

    day_1.day_exercises = [ex_1_1, ex_1_2, ex_1_3, ex_1_4, ex_1_5, ex_1_6]
    day_2.day_exercises = [ex_2_1, ex_2_2, ex_2_3, ex_2_4, ex_2_5, ex_2_6]
    day_3.day_exercises = [ex_3_1, ex_3_2, ex_3_3, ex_3_4, ex_3_5, ex_3_6]

    workout = Workout(
        user_id=user.id,
        name="testworkout",
        description="testdescription",
        training_days=[
            day_1, day_2,day_3        
        ]
    ) 

    db_session.add(workout)
    await db_session.flush()

    stmt = (
        select(Workout)
        .where(Workout.id == workout.id)
        .options(
            selectinload(Workout.training_days)
            .selectinload(TrainingDay.day_exercises)
        )
    )
    workout = await db_session.execute(stmt)
    await db_session.commit()
    return workout.scalar()

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
async def random_workouts(user: User, db_session: AsyncSession, faker: Faker):
    workouts = []
    for i in range(1, 11):
        workout = Workout(
            id=i, 
            user_id=user.id, 
            name=faker.catch_phrase(),
            description=faker.paragraph(nb_sentences=3),
            public=random.choice([True, False])
        )
        db_session.add(workout)
        await db_session.flush()
            
        workouts.append(workout)
        
    return workouts

@pytest.fixture
def uow(db_session):
    return UnitOfWork(session_maker=async_session_factory)

@pytest.fixture
def redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

@dataclass
class TrDayData:
    user_id: uuid.UUID 
    workout_id: int
    histories: list

@pytest.fixture
async def tr_day_history(workout: Workout, db_session):
    days = [
        workout.training_days[0],
        workout.training_days[1],
        workout.training_days[2]
    ]
    histories = []
    for day in days:
        history = TrainingDayHistory(
            day_id=day.id,
            day_name=day.name
        )
        histories.append(history)
        db_session.add(history)

    await db_session.flush()

    exercise_history = ExerciseHistory(
        user_id=workout.user_id,
        exercise_id=workout.training_days[0].day_exercises[0].exercise_id,
        training_day_history_id=histories[0].id,
        weight=10.0,
        sets=3,
        reps=10
    )
    db_session.add(exercise_history)

    await db_session.flush()

    data = TrDayData(
        user_id=workout.user_id,
        workout_id=workout.id,
        histories=histories
    )
    return data

