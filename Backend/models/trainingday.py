from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .workout import Workout
    from .dayexercise import DayExercise    
    from .training_day_history import TrainingDayHistory

class TrainingDay(Base):
    __tablename__ = "trainingday"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout.id", ondelete="CASCADE"),
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
    training_days_history: Mapped["TrainingDayHistory"] = relationship(
        back_populates="training_day"
    )

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "day_order",
            name="uq_workout_day_order"
        ),
    )
