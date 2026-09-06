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
from Backend.schemas.AnalyticsHistory import CreateHistory, HistoryResponse
from Backend.schemas.training_day_history import (
    ListTrDayHistoryResponse,
    TrainingDayHistoryCreate,
    TrainingDayHistoryGetAll,
    TrainingDayHistoryGetAllDTO,
    TrainingDayHistoryResponse,
    TrainingDayRelationHistoryResponse,
)
from Backend.services.AnalyticsHistoryService import AnalyticsHistoryService
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService


class TrainingDayHistoryCacheProxy(BaseCacheProxy[TrainingDayHistoryResponse]):
    def __init__(
        self,
        tr_day_service: TrainingDayHistoryService,
        analytics_service: AnalyticsHistoryService,
        redis: Redis,
        invalidator: TrainingDayHistoryCacheInvalidator,
        formatter: TrainingDayHistoryCacheKeyFormatter,
    ) -> None:
        self.tr_day_service = tr_day_service
        self.analytics_service = analytics_service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis, TrainingDayHistoryResponse)

    async def create_history(
        self, user_id: UUID, data: CreateHistory
    ) -> HistoryResponse:
        history = await self.analytics_service.create_history(user_id, data)

        await self.invalidator.invalidate_get_all(user_id)

        return HistoryResponse.model_validate(history)

    async def get_loaded_tr_day_history(
        self, user_id: UUID, history_id: int
    ) -> TrainingDayRelationHistoryResponse:
        key = self.formatter.get_loaded_key(history_id)

        history = await self._wrap_cache(
            key=key,
            response_model=TrainingDayRelationHistoryResponse,
            db_func=partial(self.tr_day_service.get_loaded_tr_day_history, history_id),
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
            db_func=partial(self.tr_day_service.get_all_tr_day_history, data_dto),
        )

    async def delete_history(
        self, user_id: UUID, history_id: int
    ) -> TrainingDayHistoryResponse:
        history = await self.tr_day_service.delete_history(history_id)

        await self.invalidator.invalidate_all(user_id, history_id)

        return self.scheme.model_validate(history)
