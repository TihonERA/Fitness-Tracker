from httpx import AsyncClient
import pytest
from uuid import UUID

from Backend.models.user import User

@pytest.mark.asyncio(loop_scope="session")
class TestUser:

    async def test_get_me(self, client: AsyncClient, user_authorized):
        response = await client.get("/users/me")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_user(self, client: AsyncClient, user_authorized):
        user = await client.get("/users/me")
        user_id = user.json().get("id")
        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_delete_user(self, client: AsyncClient, user_authorized):
        response = await client.delete("/users/me")

        deleted_user = await client.get("/users/me")

        assert response.status_code == 200
        assert deleted_user.status_code == 404
