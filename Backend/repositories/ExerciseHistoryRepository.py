from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.models.sets_history import SetsHistory
from Backend.repositories.SqlAlchemyAbstractRepository import SQLAlchemyAbstractRepository

from Backend.models.exercise_history import ExerciseHistory
from Backend.schemas.exercise_history import ExerciseHistoryCreateDTO
from Backend.utils.exceptions import DBErrorHandler

class ExerciseHistoryRepository(SQLAlchemyAbstractRepository[ExerciseHistory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ExerciseHistory)

    async def create_exercise_history(self, data: ExerciseHistoryCreateDTO) -> ExerciseHistory:
        exercise_history = ExerciseHistory(
            user_id=data.user_id,
            exercise_id=data.exercise_id,
            training_day_history_id=data.training_day_history_id
        )
        for s in data.sets_history:
            set_history = SetsHistory(**s.model_dump())
            exercise_history.sets_history.append(set_history)

        try:
            await self._add_and_refresh_instance(exercise_history, attribute_names=["sets_history"])
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)

        return exercise_history
