import pytest

from Backend.models.user import User
from Backend.schemas.user import UserCreateDB
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


        
