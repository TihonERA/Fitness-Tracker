from Backend.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Text
from .trainingday import TrainingDay

class Workout(Base):
    __tablename__ = "workout"

    workout_id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
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
    rate: Mapped[float] = mapped_column(
        Float(precision=2),
        default=0.0,
        nullable=False,
        comment="Оценка от 0 до 10"
    )

    training_days: Mapped[list["TrainingDay"]] = relationship(back_populates="workout")
