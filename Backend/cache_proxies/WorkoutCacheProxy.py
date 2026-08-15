import asyncio
from functools import partial
from types import CoroutineType
from typing import Any, Awaitable, Coroutine
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.CacheBaseProxy import CacheBaseProxy

from Backend.cache_proxies.invalidators.CacheWorkoutInvalidator import CacheWorkoutInvalidator
from Backend.cache_proxies.key_formatters.WorkoutCacheKeyFormatter import WorkoutCacheKeyFormatter
from Backend.models.workout import Workout

from Backend.schemas.workout import ListWorkoutResponse, WorkoutCreate, WorkoutGetAllFilter, WorkoutGetAllFilterDTO, WorkoutRelationsResponse, WorkoutResponse, WorkoutUpdate
from Backend.utils.uow import UnitOfWork

from Backend.services.WorkoutService import WorkoutService

class WorkoutCacheProxy(CacheBaseProxy):
    def __init__(
        self, 
        service: WorkoutService, 
        redis: Redis, 
        invalidator: CacheWorkoutInvalidator,
        formatter: WorkoutCacheKeyFormatter
    ) -> None:
        self.service = service
        self.invalidator = invalidator
        self.formatter = formatter
        super().__init__(redis=redis, scheme=WorkoutResponse)

    async def create_workout(
        self,
        user_id: UUID,
        data: WorkoutCreate
    ) -> Workout:
        db_data = await self.service.create_workout(
            user_id=user_id,
            data=data
        )

        await self.invalidator.invalidate_workouts_all(user_id=user_id)

        return db_data

    async def get_loaded_workout(
        self,
        user_id: UUID,
        workout_id: int
    ) -> str:
        key = self.formatter.get_loaded_workout_key(user_id=user_id, workout_id=workout_id)

        return await self._wrap_cache(
            key=key,
            response_model=WorkoutRelationsResponse,
            db_func=partial(self.service.get_loaded_workout, workout_id, user_id)
        )

    
    async def get_all_workouts(
        self,
        user_id: UUID,
        data: WorkoutGetAllFilter
    ) -> str:
        data_dto = WorkoutGetAllFilterDTO(
            skip=data.skip,
            limit=data.limit,
            owner_id=user_id,
            target_user_id=data.user_id,
            public=data.public
        )

        version_key = self.formatter.get_workouts_version_key(target_user_id=data_dto.target_user_id)
        version = await self.get(version_key) or '0'

        key = self.formatter.get_all_workouts_key(version=version, data=data_dto)

        return await self._wrap_cache(
            key=key,
            response_model=ListWorkoutResponse,
            db_func=partial(self.service.get_all_workouts, data=data_dto)
        )
   
    async def update_workout(
        self,
        user_id: UUID,
        workout_id: int,
        data: WorkoutUpdate
    ) -> Workout:
        workout = await self.service.update_workout(
            user_id=user_id,
            workout_id=workout_id,
            data=data
        )

        await self.invalidator.invalidate_all(
            user_id=user_id, 
            workout_id=workout_id
        )

        return workout

    async def delete_workout(
        self,
        user_id: UUID,
        workout_id: int
    ) -> Workout:
        workout = await self.service.delete_workout(
            user_id=user_id,
            workout_id=workout_id
        )

        await self.invalidator.invalidate_all(
            user_id=user_id, 
            workout_id=workout_id
        )

        return workout
