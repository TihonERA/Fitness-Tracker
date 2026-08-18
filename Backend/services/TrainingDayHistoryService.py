import asyncio
from uuid import UUID

from redis.asyncio import Redis

from Backend.models.training_day_history import TrainingDayHistory

from .BaseService import BaseService

from ..utils.uow import UnitOfWork
from ..utils.exceptions import NotFound

class TrainingDayHistoryService(BaseService):
    def __init__(self, uow: UnitOfWork, redis: Redis):
        super().__init__(uow)

    async def get_loaded_tr_day_history(
        self,
        history_id: int
    ) -> TrainingDayHistory:
        async with self.uow as uow:
            return await self._get_existing_instance(
                identifier=history_id,
                repo_get_func=uow.trainingdayhistory.get_tr_day_history
            )

