import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from Backend.main import app
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
import uuid
from ..core.database import async_session_factory
from ..models.user import User
from ..core.database import async_engine 
from ..api.deps import get_db
from ..core.database import get_redis
from alembic.config import Config
from alembic import command
from pathlib import Path

alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"

@pytest.fixture(scope="function")
async def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app) #type: ignore
    async with AsyncClient(transport=transport, base_url="http://test") as c:
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
        stmt = insert(User).values(
            user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            login="test_user",
            email="test@example.com"
        ).on_conflict_do_nothing(index_elements=["user_id"])

        await session.execute(stmt) 
        await session.commit()

    yield

    async with async_engine.begin() as conn:
        await conn.rollback()

@pytest.fixture(scope="function", autouse=True)
async def clean_tables():
    yield

    async with async_engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE workout, trainingday, dayexercise CASCADE;"))

@pytest.fixture(scope="function", autouse=True)
async def clear_redis():
    redis = get_redis()

    await redis.flushall()

    await redis.aclose()

@pytest.fixture
async def make_workout_factory_returning_data(client):
    async def _make_data(name="Split", description="TestDescription...", day_name="Day1", day_order=1):
        data = {
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": name,
            "description": description,
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
        workout_data = await client.post(f"/workouts/workout_schedule", json=data)
        return workout_data
    return _make_data
