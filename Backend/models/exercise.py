from .base import Base
from .dayexercise import DayExercise
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Text, JSON

class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id: Mapped[int] = mapped_column(
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
    gif_url: Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )
    muscle_activation: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False 
    )

    day_exercises: Mapped[list["DayExercise"]] = relationship(back_populates="exercises")