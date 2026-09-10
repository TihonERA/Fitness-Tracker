from typing import Any
from uuid import UUID

from sqlalchemy import join, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload

from Backend.models.trainingday import TrainingDay
from Backend.models.workout import Workout

from .SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

class TrainingDayRepository(SQLAlchemyAbstractRepository[TrainingDay]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TrainingDay)
