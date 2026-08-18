import asyncio
from typing import Sequence
from uuid import UUID

from redis.asyncio import Redis

from Backend.models.training_day_history import TrainingDayHistory
from Backend.schemas.training_day_history import TrainingDayHistoryCreate, TrainingDayHistoryGetAll

from .BaseService import BaseService

from ..utils.uow import UnitOfWork
from ..utils.exceptions import NotFound

class TrainingDayHistoryService(BaseService):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)

    async def create_history(self, data: TrainingDayHistoryCreate) -> TrainingDayHistory:
        async with self.uow as uow:
            return await uow.trainingdayhistory.create_instance(data)

    async def get_loaded_tr_day_history(
        self,
        history_id: int
    ) -> TrainingDayHistory:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=history_id,
                repo_get_func=uow.trainingdayhistory.get_tr_day_history
            )

    async def get_all_tr_day_history(
        self,
        data: TrainingDayHistoryGetAll
    ) -> Sequence[TrainingDayHistory]:
        async with self.uow as uow:
            histories = await uow.trainingdayhistory.get_all_tr_day_history(data)

            if histories is None:
                return []

            return histories
