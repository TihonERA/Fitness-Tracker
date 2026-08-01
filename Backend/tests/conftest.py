import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from Backend.main import app
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
import uuid
from Backend.tasks.muscle_rates import cel_app
from ..models.user import User
from ..models.workout import Workout
from ..models.trainingday import TrainingDay
from ..models.dayexercise import DayExercise
from ..core.database import async_session_factory , async_engine, get_session
from ..core.database import get_redis
from alembic.config import Config
from alembic import command
from pathlib import Path

alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"

@pytest.fixture(scope="session")
def celery_app():
    return cel_app

@pytest.fixture(scope="function")
async def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = _override_get_db

    transport = ASGITransport(app=app) #type: ignore
    async with AsyncClient(transport=transport, base_url="https://test") as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def db_session():
    async with async_session_factory() as session:
        yield session
        
        await session.rollback()

@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_database():
    alembic_cfg = Config(str(alembic_ini_path))
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

    async with async_session_factory() as session:
        await session.execute(text('TRUNCATE TABLE workout, trainingday, "user" CASCADE;'))
        user = User(
            user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            email="testmail@mail.com",
            login="registration_data_login",
            hash_password="$argon2id$v=19$m=65536,t=3,p=4$b04HUqHrntSERdQIO+Nz0A$hmNV+lnF9Y6t46tCnXfBJEIxH4MEZZuE69h8RCjBmhA"
        )

        session.add(user)
        await session.commit()

    yield

@pytest.fixture(scope="function", autouse=True)
async def clear_redis():
    redis = get_redis()

    await redis.flushall()

    await redis.aclose()

@pytest.fixture
async def make_workout(db_session: AsyncSession):
    day_1 = TrainingDay(name="Тренировка спины и бицепса", day_order=1)
    day_2 = TrainingDay(name="Тренировка груди, плеч и трицепса", day_order=2)
    day_3 = TrainingDay(name="Тренировка ног и пресса", day_order=3)

    ex_1_1 = DayExercise(exercise_id=9, exercise_order=1, sets=4, reps=15, training_day=day_1)
    ex_1_2 = DayExercise(exercise_id=10, exercise_order=2, sets=4, reps=15, training_day=day_1)
    ex_1_3 = DayExercise(exercise_id=11, exercise_order=3, sets=4, reps=15, training_day=day_1)
    ex_1_4 = DayExercise(exercise_id=18, exercise_order=4, sets=4, reps=15, training_day=day_1)
    ex_1_5 = DayExercise(exercise_id=29, exercise_order=5, sets=4, reps=15, training_day=day_1)
    ex_1_6 = DayExercise(exercise_id=43, exercise_order=6, sets=4, reps=15, training_day=day_1)

    ex_2_1 = DayExercise(exercise_id=3, exercise_order=1, sets=4, reps=15, training_day=day_2)
    ex_2_2 = DayExercise(exercise_id=5, exercise_order=2, sets=4, reps=15, training_day=day_2)
    ex_2_3 = DayExercise(exercise_id=21, exercise_order=3, sets=4, reps=15, training_day=day_2)
    ex_2_4 = DayExercise(exercise_id=22, exercise_order=4, sets=4, reps=15, training_day=day_2)
    ex_2_5 = DayExercise(exercise_id=37, exercise_order=5, sets=4, reps=15, training_day=day_2)
    ex_2_6 = DayExercise(exercise_id=45, exercise_order=6, sets=4, reps=15, training_day=day_2)

    ex_3_1 = DayExercise(exercise_id=47, exercise_order=1, sets=4, reps=15, training_day=day_3)
    ex_3_2 = DayExercise(exercise_id=17, exercise_order=2, sets=4, reps=15, training_day=day_3)
    ex_3_3 = DayExercise(exercise_id=52, exercise_order=3, sets=4, reps=15, training_day=day_3)
    ex_3_4 = DayExercise(exercise_id=59, exercise_order=4, sets=4, reps=15, training_day=day_3)
    ex_3_5 = DayExercise(exercise_id=42, exercise_order=5, sets=4, reps=15, training_day=day_3)
    ex_3_6 = DayExercise(exercise_id=40, exercise_order=6, sets=4, reps=15, training_day=day_3)

    workout = Workout(
        user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        name="testworkout",
        description="testdescription",
        training_days=[day_1, day_2, day_3],
        day_exercises=[
            ex_1_1, ex_1_2, ex_1_3, ex_1_4, ex_1_5, ex_1_6,
            ex_2_1, ex_2_2, ex_2_3, ex_2_4, ex_2_5, ex_2_6,
            ex_3_1, ex_3_2, ex_3_3, ex_3_4, ex_3_5, ex_3_6
        ]
    ) 

    db_session.add(workout)
    await db_session.flush()

    stmt = (
        select(Workout)
        .where(Workout.workout_id == workout.workout_id)
        .options(
            selectinload(Workout.training_days)
            .selectinload(TrainingDay.day_exercises)
        )
    )
    workout = await db_session.execute(stmt)
    await db_session.commit()
    return workout.scalar()

@pytest.fixture
async def user(client, db_session):
    user = User(
        user_id=uuid.UUID("10000000-0000-0000-0000-000000000000"),
        email="createusermail@mail.com",
        login="create_user_login",
        hash_password="$argon2id$v=19$m=65536,t=3,p=4$b04HUqHrntSERdQIO+Nz0A$hmNV+lnF9Y6t46tCnXfBJEIxH4MEZZuE69h8RCjBmhA"
    )
    db_session.add(user)
    await db_session.commit()
    
    login_data = {
        "login_or_email": "create_user_login",
        "password": "registration_data_password"
    }

    await client.post(f"/auth/login", json=login_data)

    yield user

    stmt = (
        select(User.user_id)
        .where(User.user_id == user.user_id)
    )
    result = await db_session.execute(stmt)
    result = result.scalar_one_or_none()
    if result:
        await db_session.delete(user)
        await db_session.commit()

@pytest.fixture
async def authorize_user(client, db_session):
    async def _make_data():
        login_data = {
            "login_or_email": "registration_data_login",
            "password": "registration_data_password"
        } 
        user_data = await client.post(f"/auth/login", json=login_data)
        await db_session.commit() 
        return user_data
    return _make_data
