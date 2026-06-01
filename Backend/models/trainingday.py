from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workout import Workout
    from .dayexercise import DayExercise    

class TrainingDay(Base):
    __tablename__ = "trainingday"

    day_id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout.workout_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    day_order: Mapped[int] = mapped_column(
        nullable=False
    )

    workout: Mapped["Workout"] = relationship(
        back_populates="training_days",
    )
    day_exercises: Mapped[list["DayExercise"]] = relationship(
        back_populates="training_day",
        cascade="all, delete-orphan"
    )