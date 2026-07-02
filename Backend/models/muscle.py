from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

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
