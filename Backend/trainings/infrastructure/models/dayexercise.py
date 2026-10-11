from Backend.shared.infrastructure.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trainingday import TrainingDayModel
    from .exercise import Exercise


class DayExerciseModel(Base):
    __tablename__ = "dayexercise"

    day_id: Mapped[int] = mapped_column(
        ForeignKey("trainingday.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    exercise_order: Mapped[int] = mapped_column(nullable=False)

    training_day: Mapped["TrainingDayModel"] = relationship(
        back_populates="day_exercises"
    )
    exercises: Mapped["Exercise"] = relationship(back_populates="day_exercises")
