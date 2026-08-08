import pytest

from Backend.models.user import User
from Backend.repositories.UserRepository import UserRepository

@pytest.mark.asyncio(loop_scope="session")
class TestUserRepository:
    
    @pytest.fixture
    def repo(self, db_session) -> UserRepository:
        return UserRepository(session=db_session)
    
    async def test_get_user_by_login(
        self, 
        repo: UserRepository, 
        user: User
    ):
        fetched_user = await repo.get_user_by_login(login=user.login)

        assert fetched_user == user

    async def test_get_user_by_email(
        self,
        repo: UserRepository,
        user: User
    ):
        fetched_user = await repo.get_user_by_email(email=user.email)

        assert fetched_user == user

    async def test_check_user_exists(
        self,
        repo: UserRepository,
        user: User
    ):
        fetched_user = await repo.check_user_exists(
            login=user.login,
            email=user.email
        )

        assert fetched_user is not None

    async def test_check_user_exists_invalid(
        self,
        repo: UserRepository,
        user: User
    ):
        fetched_user = await repo.check_user_exists(
            login="wrong_login",
            email="wrongmail@mail.com"
        )

        assert fetched_user is None
