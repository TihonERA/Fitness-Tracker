from .base import Base
from .trainingday import TrainingDay
from .exercise import Exercise
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class DayExercise(Base):
    __tablename__ = "dayexercise"

    day_id: Mapped[int] = mapped_column(
        ForeignKey("trainingday.day_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.exercise_id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    exercise_order: Mapped[int] = mapped_column(
        nullable=False
    )
    sets: Mapped[int|None] = mapped_column(
        default=None,
    )
    reps: Mapped[int|None] = mapped_column(
        default=None
    )

    training_days: Mapped["TrainingDay"] = relationship(back_populates="day_exercises")
    exercises: Mapped["Exercise"] = relationship(back_populates="day_exercises")