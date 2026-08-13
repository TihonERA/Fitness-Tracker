import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from Backend.models.workout import Workout
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO, TrainingDayUpdate
from Backend.services.BaseService import BaseService
from Backend.services.DayExerciseService import DayExerciseService
from Backend.utils.uow import UnitOfWork
from ..utils.exceptions import Forbidden, InternalServerError, NotFound
from ..repositories.TrainingDayRepository import TrainingDayRepository
from ..models.trainingday import TrainingDay

class TrainingDayService(BaseService):

    def __init__(self, uow: UnitOfWork, redis: Redis):
        super().__init__(uow)

    async def get_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ) -> TrainingDay:
        async with self.uow as uow:
            await self._get_instance_with_access(
                identifier=workout_id,
                user_id=user_id,
                repo_get_func=uow.workout.get_instance_by_id
            )
            return await self._get_existing_instance(
                identifier=day_id,
                repo_get_func=uow.trainingday.get_loaded_training_day
            )

    async def create_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        data: TrainingDayCreateDTO
    ) -> TrainingDay:
        async with self.uow as uow:
            await self._get_instance_with_access(
                identifier=workout_id,
                user_id=user_id,
                repo_get_func=uow.workout.get_instance_by_id
            )
            return await uow.trainingday.create_instance(
                data=data
            )

    async def update_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: TrainingDayUpdate
    ) -> TrainingDay:
        async with self.uow as uow:
            await self._get_instance_with_access(
                identifier=workout_id,
                user_id=user_id,
                repo_get_func=uow.workout.get_instance_by_id
            )
            training_day = await self._get_existing_instance(
                identifier=day_id,
                repo_get_func=uow.trainingday.get_instance_for_update
            )
            result = await uow.trainingday.update_instance(
                instance=training_day,
                data=data
            )

            return result

    async def delete_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ) -> TrainingDay:
        async with self.uow as uow:
            await self._get_instance_with_access(
                identifier=workout_id,
                user_id=user_id,
                repo_get_func=uow.workout.get_instance_by_id
            )
            training_day = await self._get_existing_instance(
                identifier=day_id,
                repo_get_func=uow.trainingday.get_instance_by_id
            )

            await uow.trainingday.delete_by_id(id=day_id)

            return training_day
