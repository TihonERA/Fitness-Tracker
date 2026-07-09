from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from .muscle import Muscle 

class MuscleAntagonists(Base):
    __tablename__ = "muscle_antagonists"

    muscle_id: Mapped[int] = mapped_column(
       ForeignKey("muscle.muscle_id", ondelete="CASCADE"),
       primary_key=True,
       index=True,
       nullable=False
    )
    muscle_antagonist_id: Mapped[int] = mapped_column(
        ForeignKey("muscle.muscle_id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        nullable=False
    )

    muscles: Mapped["Muscle"] = relationship(
        back_populates="main_muscles",
        foreign_keys=[muscle_id] 
    )
    muscles_antagonists: Mapped["Muscle"] = relationship(
        back_populates="antagonists_muscles",
        foreign_keys=[muscle_antagonist_id]
    )
            
    
