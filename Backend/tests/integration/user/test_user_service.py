import pytest

from Backend.models.user import User
from Backend.schemas.user import UserCreateDB, UserUpdate
from Backend.services.UserService import UserService
from Backend.utils.uow import UnitOfWork

@pytest.mark.asyncio(loop_scope="session")
class TestUserService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        return UserService(uow=uow)

    async def test_create_user_success(
        self, 
        service: UserService, 
        user: User
    ):
        data = UserCreateDB(
            email="mailtest@mail.com",
            login="somelogin",
            hash_password=user.hash_password
        )
        
        user = await service.create_user(data=data)

        assert user.email == data.email
        assert user.login == data.login
        assert data.hash_password == user.hash_password

    async def test_get_user_by_column(
        self, 
        service: UserService, 
        user: User
    ):
        fetched_by_id = await service.get_user_by_id(user_id=user.id)
        fetched_by_login = await service.get_user_by_login(login=user.login)
        fetched_by_email = await service.get_user_by_email(email=user.email)

        users = [fetched_by_id, fetched_by_login, fetched_by_email]
        assert all(users)
        assert fetched_by_id.id == fetched_by_login.id == fetched_by_email.id
