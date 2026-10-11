from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, String, column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backend.shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .exercise_history import ExerciseHistoryModel


class TrainingDayHistoryModel(Base):
    __tablename__ = "trainingdayhistory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    day_id: Mapped[int] = mapped_column(
        ForeignKey("trainingday.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    day_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    exercises_history: Mapped[list["ExerciseHistoryModel"]] = relationship(
        back_populates="training_day_history"
    )
