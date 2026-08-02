from typing import Any
from uuid import UUID

from sqlalchemy import select, or_

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class UserRepository(SQLAlchemyAbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def create_user(self, data: dict[str, Any]) -> User:
        return await self.create_instance(data=data)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.get_instance_by_column(
            column=User.user_id,
            identificator=user_id
        )

    async def get_user_by_login(self, login: str) -> User | None:
        return await self.get_instance_by_column(
            column=User.login,
            identificator=login
        )

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.get_instance_by_column(
            column=User.email,
            identificator=email
        )

    async def get_user_for_update(self, user_id: UUID) -> User | None:
        return await self.get_instance_for_update(
            column=User.user_id,
            identificator=user_id
        )

    async def check_user_exists(
        self,
        login: str,
        email: str,
    ) -> User | None:
        stmt = (
            select(self.model)
            .where(
                or_(
                    self.model.login == login,
                    self.model.email == email
                )
            )
        )
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user(
        self,
        user_id: UUID,
    ) -> int:
       return await self.delete_by_column(
            column=User.user_id,
            identificator=user_id
        )
    

