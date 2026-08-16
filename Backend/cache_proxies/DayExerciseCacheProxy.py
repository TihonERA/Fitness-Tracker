from uuid import UUID

from redis.asyncio import Redis

from Backend.cache_proxies.BaseCacheProxy import BaseCacheProxy
from Backend.cache_proxies.invalidators.WorkoutCacheInvalidator import WorkoutCacheInvalidator
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseCreateDTO, DayExerciseResponse
from Backend.services.DayExerciseService import DayExerciseService

class DayExerciseCacheProxy(BaseCacheProxy[DayExerciseResponse]):
    def __init__(
        self,
        service: DayExerciseService,
        redis: Redis,
        workout_invalidator: WorkoutCacheInvalidator,
    ) -> None:
        self.service = service
        self.workout_invalidator = workout_invalidator
        super().__init__(redis, DayExerciseResponse)

    async def create_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: DayExerciseCreate
    ) -> DayExerciseResponse:
        data_dto = DayExerciseCreateDTO(
            exercise_id=data.exercise_id,
            exercise_order=data.exercise_order,
            day_id=day_id
        )

        day_exercise = await self.service.create_day_exercise(
            user_id=user_id,
            workout_id=workout_id,
            data=data_dto
        )

        await self.workout_invalidator.invalidate_loaded_workout(workout_id)

        return self.scheme.model_validate(day_exercise)

    async def delete_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ) -> DayExerciseResponse:
        day_exercise = await self.service.delete_day_exercise(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id,
            exercise_id=exercise_id
        )

        await self.workout_invalidator.invalidate_loaded_workout(workout_id)

        return self.scheme.model_validate(day_exercise)
