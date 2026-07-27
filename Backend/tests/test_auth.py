import pytest

@pytest.mark.asyncio(loop_scope="session")
class TestAuthAPI:
    
    async def test_login(self, client, make_user_data):
        user_res = await make_user_data()

        login_data = {
            "login_or_email": "testmail@mail.com",
            "password": "registration_data_password"
        }
        
        response = await client.post(f"/auth/login", json=login_data) 

        assert response.status_code == 200

    async def test_registration(self, client):
        registration_data = {
            "email": "testmail@test.com",
            "login": "test_data_login",
            "password": "registration_data_password"
        }
 
        response = await client.post(f"/auth/users", json=registration_data)

        assert response.status_code == 200
