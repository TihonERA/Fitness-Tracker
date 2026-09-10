from typing import Any
from uuid import UUID

from sqlalchemy import select, or_

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class UserRepository(SQLAlchemyAbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_user_by_login(self, login: str) -> User | None:
        return await self.get_instance_by_column(
            column=User.login,
            search_value=login
        )

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.get_instance_by_column(
            column=User.email,
            search_value=email
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
