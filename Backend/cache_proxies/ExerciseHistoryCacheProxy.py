from functools import partial
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.BaseCacheProxy import BaseCacheProxy
from Backend.cache_proxies.key_formatters.ExerciseHistoryCacheKeyFormatter import (
    ExerciseHistoryCacheKeyFormatter,
)
from Backend.schemas.exercise_history import (
    ExerciseHistoryCreate,
    ExerciseHistoryCreateDTO,
    ExerciseHistoryGetAll,
    ExerciseHistoryGetAllDTO,
    ExerciseHistoryRelalationsResponse,
    ExerciseHistoryResponse,
    ListExerciseHistoryResponse,
)

from Backend.services.ExerciseHistoryService import ExerciseHistoryService
from Backend.cache_proxies.invalidators.ExerciseHistoryCacheInvalidator import (
    ExerciseHistoryCacheInvalidator,
)


class ExerciseHistoryCacheProxy(BaseCacheProxy[ExerciseHistoryResponse]):
    def __init__(
        self,
        service: ExerciseHistoryService,
        redis: Redis,
        invalidator: ExerciseHistoryCacheInvalidator,
        formatter: ExerciseHistoryCacheKeyFormatter,
    ) -> None:
        self.service = service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis, ExerciseHistoryResponse)

    async def create_exercise_history(
        self, user_id: UUID, data: ExerciseHistoryCreate
    ) -> ExerciseHistoryRelalationsResponse:
        data_dto = ExerciseHistoryCreateDTO(user_id=user_id, **data.model_dump())
        exercise_history = await self.service.create_exercise_history(data_dto)

        await self.invalidator.invalidate_get_all(user_id)

        return ExerciseHistoryRelalationsResponse.model_validate(exercise_history)

    async def get_exercise_history(
        self, user_id: UUID, history_id: int
    ) -> ExerciseHistoryRelalationsResponse:
        key = self.formatter.get_loaded_key(history_id)

        history = await self._wrap_cache(
            key=key,
            response_model=ExerciseHistoryRelalationsResponse,
            db_func=partial(self.service.get_exercise_history, history_id),
        )

        tag_key = self.formatter.get_tag_key(user_id)
        await self.sadd(tag_key, key)

        return history

    async def get_all_exercise_history(
        self, user_id: UUID, data: ExerciseHistoryGetAll
    ) -> ListExerciseHistoryResponse:
        data_dto = ExerciseHistoryGetAllDTO(user_id=user_id, **data.model_dump())

        version_key = self.formatter.get_version_key(user_id)
        version = await self.get(version_key) or "0"

        key = self.formatter.get_all_key(version, data_dto)

        return await self._wrap_cache(
            key=key,
            response_model=ListExerciseHistoryResponse,
            db_func=partial(self.service.get_all_histories, data_dto),
        )

    async def delete_history(
        self, user_id: UUID, history_id: int
    ) -> ExerciseHistoryResponse:
        history = await self.service.delete_history(history_id)

        await self.invalidator.invalidate_all(user_id, history_id)

        return self.scheme.model_validate(history)
