from httpx import AsyncClient
import pytest

from Backend.models.user import User

@pytest.mark.asyncio(loop_scope="session")
class TestUser:

    async def test_get_me(self, client: AsyncClient, authorize_user):
        await authorize_user()
        response = await client.get("/users/me")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_user(self, client: AsyncClient, authorize_user):
        await authorize_user()
        user = await client.get("/users/me")
        user_id = user.json().get("user_id")
        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_update_user(self, client: AsyncClient, user):
        update_data = {
            "login": "newupdatedlogin"
        }
        response = await client.patch("/users/me", json=update_data)

        assert response.status_code == 200
        assert response.json().get("login") == update_data.get("login")

    async def test_delete_user(self, client: AsyncClient, user: User):
        print(f"\n{[getattr(user, attr) for attr in user.__table__.columns.keys()]}")
        response = await client.delete("/users/me")

        deleted_user = await client.get("/users/me")

        assert response.status_code == 200
        assert deleted_user.status_code == 404
