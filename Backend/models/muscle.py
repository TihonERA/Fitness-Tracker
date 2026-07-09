from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .muscle_antagonists import MuscleAntagonists

class Muscle(Base):
    __tablename__ = "muscle"

    muscle_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        index=True,
        nullable=False
    )

    main_muscles: Mapped[list["MuscleAntagonists"]] = relationship(
        back_populates="muscles",
        foreign_keys="[MuscleAntagonists.muscle_id]"
    )

    antagonists_muscles: Mapped[list["MuscleAntagonists"]] = relationship(
        back_populates="muscles_antagonists",
        foreign_keys="[MuscleAntagonists.muscle_antagonist_id]"
    )
