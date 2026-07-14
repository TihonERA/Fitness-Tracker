from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar

class Base(DeclarativeBase):
    pass

ModelT = TypeVar("ModelT", bound=Base)
