from functools import partial
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.BaseCacheProxy import BaseCacheProxy
from Backend.cache_proxies.invalidators.TrainingDayHistoryCacheInvalidator import (
    TrainingDayHistoryCacheInvalidator,
)
from Backend.cache_proxies.key_formatters.TrainingDayHistoryCacheKeyFormatter import (
    TrainingDayHistoryCacheKeyFormatter,
)
from Backend.models.training_day_history import TrainingDayHistory
from Backend.schemas.training_day_history import (
    ListTrDayHistoryResponse,
    TrainingDayHistoryCreate,
    TrainingDayHistoryGetAll,
    TrainingDayHistoryGetAllDTO,
    TrainingDayHistoryResponse,
)
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService


class TrainingDayHistoryCacheProxy(BaseCacheProxy[TrainingDayHistoryResponse]):
    def __init__(
        self,
        service: TrainingDayHistoryService,
        redis: Redis,
        invalidator: TrainingDayHistoryCacheInvalidator,
        formatter: TrainingDayHistoryCacheKeyFormatter,
    ) -> None:
        self.service = service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis, TrainingDayHistoryResponse)

    async def create_history(
        self, user_id: UUID, data: TrainingDayHistoryCreate
    ) -> TrainingDayHistoryResponse:
        history = await self.service.create_history(data)

        await self.invalidator.invalidate_get_all(user_id)

        return self.scheme.model_validate(history)

    async def get_loaded_tr_day_history(
        self, user_id: UUID, history_id: int
    ) -> TrainingDayHistoryResponse:
        key = self.formatter.get_loaded_key(history_id)

        history = await self._wrap_cache(
            key=key, db_func=partial(self.service.get_loaded_tr_day_history, history_id)
        )

        tag_key = self.formatter.get_tag_key(user_id)
        await self.sadd(tag_key, key)

        return history

    async def get_all_tr_day_history(
        self, user_id: UUID, data: TrainingDayHistoryGetAll
    ) -> ListTrDayHistoryResponse:
        data_dto = TrainingDayHistoryGetAllDTO(
            user_id=user_id, **data.model_dump(exclude_unset=True)
        )
        version_key = self.formatter.get_version_key(user_id)
        version = await self.get(version_key) or "0"

        key = self.formatter.get_all_key(version=version, data=data_dto)

        return await self._wrap_cache(
            key=key,
            response_model=ListTrDayHistoryResponse,
            db_func=partial(self.service.get_all_tr_day_history, data_dto),
        )

    async def delete_history(
        self, user_id: UUID, history_id: int
    ) -> TrainingDayHistoryResponse:
        history = await self.service.delete_history(history_id)

        await self.invalidator.invalidate_all(user_id, history_id)

        return self.scheme.model_validate(history)
