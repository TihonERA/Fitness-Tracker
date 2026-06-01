from Backend.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workout import Workout

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    login: Mapped[str] = mapped_column(
        String(32),
        index=True,
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False
    )

    workouts: Mapped[list["Workout"]] = relationship(back_populates="user")