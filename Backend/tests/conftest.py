import pytest
from httpx import AsyncClient, ASGITransport
from Backend.main import app
from sqlalchemy import text
import uuid
from ..core.database import async_session_factory
from ..models.base import Base
from ..models.user import User
from ..models.exercise import Exercise
from ..core.database import async_engine 
from ..api.deps import get_db
from ..core.database import get_redis

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
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    async with async_session_factory() as session:
        user = User(
            user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            login="test_user",
            email="test@example.com"
        )

        push_ups = Exercise(
            name="push_ups",
            muscle_activation={
                "pectoralis_major": 0.45,
                "triceps": 0.35,
                "anterior_deltoid": 0.20
            }
        )

        Dumbbell_Bicep_Curl = Exercise(
            name="Dumbbell_Bicep_Curl",
            muscle_activation={
                "biceps_brachii": 0.80,
                "brachialis": 0.20
            }
        )

        Crunches = Exercise(
            name="Crunches",
            muscle_activation={
                "rectus_abdominis": 0.80,
                "obliques": 0.20
            }
        )
        
        session.add_all([user, push_ups, Dumbbell_Bicep_Curl, Crunches])
        
        await session.commit()

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

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
            "training_days": [{
                "name": day_name,
                "day_order": day_order,
                "day_exercises": [{
                    "exercise_id": 1,
                    "exercise_order": 1,
                    "sets": 4,
                    "reps": 15
                }]
            }]
        }

        workout_data = await client.post(f"/workouts/workout_schedule", json=data)
        return workout_data
    return _make_data
