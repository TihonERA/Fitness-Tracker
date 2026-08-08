from pydantic import BaseModel
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import random

from Backend.models.base import Base
from Backend.models.workout import Workout
from Backend.repositories.SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

from faker import Faker

class DummyModel(Base):
    __tablename__ = "dummy_table"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(nullable=False)

class DummyRepository(SQLAlchemyAbstractRepository[DummyModel]):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=DummyModel)

@pytest.mark.asyncio(loop_scope="session")
class TestAbstractRepository:

    @pytest.fixture
    def repo(self, db_session: AsyncSession) -> DummyRepository:
        return DummyRepository(session=db_session)

    @pytest.fixture
    def fake_dto(self, faker, repo, mocker):
        name = faker.name()
        
        data = mocker.MagicMock()
        data.model_dump.return_value = {"name": name}

        return data

    @pytest.fixture
    async def created_instance(self, db_session, faker, repo, mocker, fake_dto):
        data = fake_dto

        instance = await repo.create_instance(data=data)
        await db_session.flush()

        return instance
    
    async def test_create_instance(self, db_session, repo, fake_dto):
        data = fake_dto

        instance = await repo.create_instance(data=data)
        await db_session.flush()

        assert instance.name == data.model_dump().get("name")

    async def test_get_instance(self, db_session, faker, repo, mocker, created_instance):
        get_instance = await repo.get_instance_by_id(id=created_instance.id)

        assert created_instance == get_instance

    async def test_get_instance_invalid(self, db_session, repo):
        fake_id = random.randint(1, 100)

        get_instance = await repo.get_instance_by_id(id=fake_id)

        assert get_instance is None

    async def test_update_instance(self, db_session, repo, fake_dto, created_instance):
        data = fake_dto

        updated_instance = await repo.update_instance(
            instance=created_instance,
            data=data
        )

        assert updated_instance.name == data.model_dump().get("name")

    async def test_delete_by_id(self, db_session, repo, created_instance):
        assert_instance_exist = await repo.get_instance_by_id(id=created_instance.id)

        assert assert_instance_exist is not None

        await repo.delete_by_id(id=created_instance.id)

        assert_instance_deleted = await repo.get_instance_by_id(id=created_instance.id)

        assert assert_instance_deleted is None

    async def test_delete_by_id_invalid(self, db_session, repo, created_instance):
        fake_id = random.randint(1, 100)
        while fake_id == created_instance.id:
            fake_id = random.randint(1, 100)

        await repo.delete_by_id(id=fake_id)

        get_instance = await repo.get_instance_by_id(id=created_instance.id)

        assert get_instance is not None
