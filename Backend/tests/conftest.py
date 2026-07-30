import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from Backend.main import app
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
import uuid
from Backend.tasks.muscle_rates import cel_app
from ..models.user import User
from ..models.workout import Workout
from ..models.trainingday import TrainingDay
from ..models.dayexercise import DayExercise
from ..core.database import async_session_factory , async_engine
from ..api.deps import get_session
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
async def setup_and_teardown_database(workout_data):
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

        workout = Workout(
            user_id=user.user_id,
            name=workout_data.get("name"),
            description=workout_data.get("description")
        )

        session.add_all([workout, user])
        await session.flush()

        for tr_day in workout_data.get("training_days", []):
            training_day = TrainingDay(
                name=tr_day.get("name"),
                day_order=tr_day.get("day_order"),
                workout_id=workout.workout_id
            )
            session.add(training_day)
            await session.flush()

            for day_ex in tr_day.get("day_exercises", []):
                day_exercise = DayExercise(
                    day_id=training_day.day_id,
                    exercise_id=day_ex.get("exercise_id"),
                    workout_id=workout.workout_id,
                    exercise_order=day_ex.get("exercise_order"),
                    sets=day_ex.get("sets"),
                    reps=day_ex.get("reps")
                )
                session.add(day_exercise)

        await session.commit()

    yield

@pytest.fixture(scope="function", autouse=True)
async def clear_redis():
    redis = get_redis()

    await redis.flushall()

    await redis.aclose()

@pytest.fixture(scope="session")
def workout_data():
    data = {
        "user_id": "00000000-0000-0000-0000-000000000000",
        "name": "testworkout",
        "description": "testdescriptiontestdescriptiontestdescription",
        "training_days": [
            {
                "name": "Тренировка спины и бицепса",
                "day_order": 1,
                "day_exercises": [
                    {"exercise_id": 9, "exercise_order": 1, "sets": 4, "reps": 15},  
                    {"exercise_id": 10, "exercise_order": 2, "sets": 4, "reps": 15},
                    {"exercise_id": 11, "exercise_order": 3, "sets": 4, "reps": 15}, 
                    {"exercise_id": 18, "exercise_order": 4, "sets": 4, "reps": 15}, 
                    {"exercise_id": 29, "exercise_order": 5, "sets": 4, "reps": 15}, 
                    {"exercise_id": 43, "exercise_order": 6, "sets": 4, "reps": 15}  
                ]
            },
            {
                "name": "Тренировка груди, плеч и трицепса",
                "day_order": 2,
                "day_exercises": [
                    {"exercise_id": 3, "exercise_order": 1, "sets": 4, "reps": 15}, 
                    {"exercise_id": 5, "exercise_order": 2, "sets": 4, "reps": 15}, 
                    {"exercise_id": 21, "exercise_order": 3, "sets": 4, "reps": 15},
                    {"exercise_id": 22, "exercise_order": 4, "sets": 4, "reps": 15},
                    {"exercise_id": 37, "exercise_order": 5, "sets": 4, "reps": 15},  
                    {"exercise_id": 45, "exercise_order": 6, "sets": 4, "reps": 15}  
                ]
            },
            {
                "name": "Тренировка ног и пресса",
                "day_order": 3,
                "day_exercises": [
                    {"exercise_id": 47, "exercise_order": 1, "sets": 4, "reps": 15}, 
                    {"exercise_id": 17, "exercise_order": 2, "sets": 4, "reps": 15}, 
                    {"exercise_id": 52, "exercise_order": 3, "sets": 4, "reps": 15}, 
                    {"exercise_id": 59, "exercise_order": 4, "sets": 4, "reps": 15}, 
                    {"exercise_id": 42, "exercise_order": 5, "sets": 4, "reps": 15}, 
                    {"exercise_id": 40, "exercise_order": 6, "sets": 4, "reps": 15}  
                ]
            }
            ]
        } 
    return data

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
