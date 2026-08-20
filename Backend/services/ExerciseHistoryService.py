from typing import Sequence

from Backend.schemas.exercise_history import ExerciseHistoryCreateDTO, ExerciseHistoryGetAllDTO
from Backend.services.BaseService import BaseService

from Backend.models.exercise_history import ExerciseHistory
from Backend.utils.exceptions import NotFound
from Backend.utils.uow import UnitOfWork

class ExerciseHistoryService(BaseService[ExerciseHistory]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)

    async def create_exercise_history(self, data: ExerciseHistoryCreateDTO) -> ExerciseHistory:
        async with self.uow as uow:
            return await uow.exercisehistory.create_exercise_history(data)

    async def get_exercise_history(self, history_id: int) -> ExerciseHistory:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=history_id,
                repo_get_func=uow.exercisehistory.get_exercise_history
            )

    async def get_all_histories(self, data: ExerciseHistoryGetAllDTO) -> Sequence[ExerciseHistory]:
        async with self.uow as uow:
            histories = await uow.exercisehistory.get_all_histories(data)

            if histories is None:
                return []

            return histories

    async def delete_history(self, history_id: int) -> ExerciseHistory:
        async with self.uow as uow:
            history = await uow.exercisehistory.get_instance_for_update(history_id)

            if history is None:
                raise NotFound()

            await uow.exercisehistory.delete_by_id(history_id)

            return history
