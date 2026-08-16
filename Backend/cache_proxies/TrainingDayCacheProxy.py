from functools import partial
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.BaseCacheProxy import BaseCacheProxy
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator 
from Backend.cache_proxies.invalidators.TrainingDayCacheInvalidator import TrainingDayCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayCacheKeyFormatter import TrainingDayCacheKeyFormatter
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO, TrainingDayRelataionsResponse, TrainingDayResponse
from Backend.services.TrainingDayService import TrainingDayService


class TrainingDayCacheProxy(BaseCacheProxy[TrainingDayResponse]):
    def __init__(
        self,
        service: TrainingDayService, 
        redis: Redis,
        invalidator: TrainingDayCacheInvalidator,
        workout_invalidator: WorkoutCacheInvalidator,
        formatter: TrainingDayCacheKeyFormatter
    ) -> None:
        self.service = service
        self.workout_invalidator = workout_invalidator
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis, TrainingDayResponse)

    async def create_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        data: TrainingDayCreate 
    ) -> TrainingDayResponse:
        data_dto = TrainingDayCreateDTO(
            name=data.name,
            day_order=data.day_order,
            workout_id=workout_id
        )
            
        training_day = await self.service.create_training_day(
            user_id=user_id,
            data=data_dto
        )

        await self.workout_invalidator.invalidate_loaded_workout(workout_id)
        
        return self.scheme.model_validate(training_day)

    async def test_get_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ) -> TrainingDayRelataionsResponse:
        key = self.formatter.get_loaded_tr_day_key(day_id)

        return await self._wrap_cache(
            key=key,
            response_model=TrainingDayRelataionsResponse,
            db_func=partial(self.service.get_loaded_training_day, user_id, workout_id, day_id)
        )
