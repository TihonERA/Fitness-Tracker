from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .user import User
    from .training_day_history import TrainingDayHistory
    from .exercise import Exercise
    
class ExerciseHistory(Base):
    __tablename__ = "exercisehistory"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    training_day_history_id: Mapped[int] = mapped_column(
        ForeignKey("trainingdayhistory.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    weight: Mapped[float] = mapped_column(
        Float(precision=2),
        default=0.0, 
        nullable=True
    )
    sets: Mapped[int] = mapped_column(nullable=True)
    reps: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(
        back_populates="exercises_history",
    )
    exercise: Mapped["Exercise"] = relationship(
        back_populates="exercises_history"
    )
    training_day_history: Mapped["TrainingDayHistory"] = relationship(
        back_populates="exercises_history"
    )
