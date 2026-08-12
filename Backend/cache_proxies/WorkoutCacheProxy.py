import asyncio
from functools import partial
from types import CoroutineType
from typing import Any, Awaitable, Coroutine
from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.CacheBaseProxy import CacheBaseProxy

from Backend.models.workout import Workout

from Backend.schemas.workout import ListWorkoutResponse, WorkoutCachePrefixes, WorkoutCreate, WorkoutGetAllFilter, WorkoutGetAllFilterDTO, WorkoutRelationsResponse, WorkoutResponse, WorkoutUpdate
from Backend.utils.uow import UnitOfWork

from Backend.services.WorkoutService import WorkoutService

class WorkoutCacheProxy(CacheBaseProxy[Workout]):
    def __init__(self, uow: UnitOfWork, redis: Redis) -> None:
        self.workout_service = WorkoutService(uow=uow)
        super().__init__(redis=redis, scheme=WorkoutResponse)

    async def create_workout(
        self,
        user_id: UUID,
        data: WorkoutCreate
    ) -> Workout:
        db_data = await self.workout_service.create_workout(
            user_id=user_id,
            data=data
        )

        await self.delete_searching_with_pattern(
            prefix=WorkoutCachePrefixes.all_workouts,
            user_id=user_id
        )

        return db_data

    async def get_loaded_workout(
        self,
        user_id: UUID,
        workout_id: int
    ) -> str:
        key = self.formate_key(
            prefix=WorkoutCachePrefixes.loaded_workout,
            user_id=user_id,
            workout_id=workout_id
        )

        origin_call = partial(
            self.workout_service.get_loaded_workout,
            user_id=user_id,
            workout_id=workout_id
        )

        return await self._wrap_cache(
            key=key,
            response_model=WorkoutRelationsResponse,
            db_func=origin_call
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

        version_key = self.formate_key(
            prefix=WorkoutCachePrefixes.version,
            user_id=data_dto.target_user_id
        )
        version = await self.get(version_key) or '0'

        key = self.formate_key(
            prefix=WorkoutCachePrefixes.all_workouts,
            version=version,
            data=data_dto.model_dump()
        )
        origin_call = partial(
            self.workout_service.get_all_workouts,
            user_id=user_id,
            data=data_dto
        )

        return await self._wrap_cache(
            key=key,
            response_model=ListWorkoutResponse,
            db_func=origin_call
        )

    async def invalidate_workout_cache(
        self,
        user_id: UUID,
        workout_id: int
    ) -> None:
        loaded_workout_key = self.formate_key(
            prefix=WorkoutCachePrefixes.loaded_workout, 
            workout_id=workout_id
        )
        workouts_all_key = self.formate_key(
            prefix=WorkoutCachePrefixes.all_workouts,
            user_id=user_id
        )
        await asyncio.gather(
            self.redis.delete(loaded_workout_key),
            self.redis.incr(workouts_all_key)
        )
        
    async def update_workout(
        self,
        user_id: UUID,
        workout_id: int,
        data: WorkoutUpdate
    ) -> Workout:
        workout = await self.workout_service.update_workout(
            user_id=user_id,
            workout_id=workout_id,
            data=data
        )

        await self.invalidate_workout_cache(user_id=user_id, workout_id=workout_id)

        return workout

    async def delete_workout(
        self,
        user_id: UUID,
        workout_id: int
    ) -> Workout:
        workout = await self.workout_service.delete_workout(
            user_id=user_id,
            workout_id=workout_id
        )

        await self.invalidate_workout_cache(user_id=user_id, workout_id=workout_id)

        return workout
