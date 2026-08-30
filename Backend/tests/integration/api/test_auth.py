from httpx import AsyncClient
from Backend.models.user import User
import pytest


@pytest.mark.asyncio(loop_scope="session")
class TestAuthAPI:

    async def test_login(self, client: AsyncClient, user: User):
        login_data = {
            "login_or_email": user.login,
            "password": "registration_data_password",
        }

        response = await client.post(f"/auth/login", json=login_data)

        assert response.status_code == 200

    async def test_registration(self, client):
        registration_data = {
            "email": "testmail@test.com",
            "login": "test_data_login",
            "password": "registration_data_password",
        }

        response = await client.post(f"/auth/users", json=registration_data)

        assert response.status_code == 200

    async def test_update_password(self, client: AsyncClient, user_authorized):
        update_data = {
            "old_password": "registration_data_password",
            "password": "new_good_password1111",
        }
        response = await client.patch("/auth/me/password", json=update_data)

        assert response.status_code == 200
