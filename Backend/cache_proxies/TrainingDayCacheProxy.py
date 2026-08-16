from functools import partial
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.BaseCacheProxy import BaseCacheProxy
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator 
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO, TrainingDayRelataionsResponse, TrainingDayResponse, TrainingDayUpdate
from Backend.services.TrainingDayService import TrainingDayService


class TrainingDayCacheProxy(BaseCacheProxy[TrainingDayResponse]):
    def __init__(
        self,
        service: TrainingDayService, 
        redis: Redis,
        workout_invalidator: WorkoutCacheInvalidator,
    ) -> None:
        self.service = service
        self.workout_invalidator = workout_invalidator
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

    async def update_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: TrainingDayUpdate
    ) -> TrainingDayResponse:
        training_day = await self.service.update_training_day(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id,
            data=data
        )

        await self.workout_invalidator.invalidate_loaded_workout(workout_id=workout_id)

        return self.scheme.model_validate(training_day)

    async def delete_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ) -> TrainingDayResponse:
        training_day = await self.service.delete_training_day(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id,
        )

        await self.workout_invalidator.invalidate_loaded_workout(workout_id=workout_id)

        return self.scheme.model_validate(training_day)
