from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .exercise_history import ExerciseHistory

class SetsHistory(Base):
    __tablename__ = "setshistory"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    exercise_history_id: Mapped[int] = mapped_column(
        ForeignKey("exercisehistory.id"),
        index=True,
        nullable=False
    )
    set: Mapped[int] = mapped_column(nullable=True)
    reps: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(Float(2), nullable=True)
    time_for_set: Mapped[datetime] = mapped_column(nullable=True)

    exercise_history: Mapped["ExerciseHistory"] = relationship(
        back_populates="sets_history"
    )
