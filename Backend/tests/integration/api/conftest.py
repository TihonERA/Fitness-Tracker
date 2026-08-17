from Backend.tasks.muscle_rates import cel_app

from httpx import AsyncClient, ASGITransport

from Backend.main import app


import pytest

@pytest.fixture
async def user_authorized(client, user):
    login_data = {
        "login_or_email": user.login,
        "password": "registration_data_password"
    }

    await client.post(f"/auth/login", json=login_data)

    yield user

@pytest.fixture(scope="session")
def celery_app():
    return cel_app

@pytest.fixture(scope="function")
async def client(db_session):
    transport = ASGITransport(app=app) #type: ignore
    async with AsyncClient(transport=transport, base_url="https://test") as c:
        yield c
