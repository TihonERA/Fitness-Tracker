from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backend.shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .training_day_history import TrainingDayHistoryModel
    from .sets_history import SetsHistory


class ExerciseHistoryModel(Base):
    __tablename__ = "exercisehistory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    training_day_history_id: Mapped[int | None] = mapped_column(
        ForeignKey("trainingdayhistory.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    training_day_history: Mapped["TrainingDayHistoryModel"] = relationship(
        back_populates="exercises_history"
    )
    sets_history: Mapped[list["SetsHistory"]] = relationship(
        back_populates="exercise_history", cascade="all, delete-orphan"
    )
