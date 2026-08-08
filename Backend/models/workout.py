from Backend.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Text, ForeignKey
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trainingday import TrainingDay
    from .dayexercise import DayExercise
    from .user import User

class Workout(Base):
    __tablename__ = "workout"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100), 
        index=True,
        nullable=False
    )
    description: Mapped[str|None] = mapped_column(
        Text, 
        nullable=True
    )
    public: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="workouts")
    training_days: Mapped[list["TrainingDay"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan"
    )
    day_exercises: Mapped[list["DayExercise"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan"
    )
