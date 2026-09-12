import asyncio
from typing import Any, Awaitable, Callable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from Backend.models.workout import Workout
from Backend.repositories import SqlAlchemyAbstractRepository
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayCreateDTO, TrainingDayUpdate
from Backend.services.BaseService import BaseService
from Backend.utils.uow import UnitOfWork
from ..utils.exceptions import Forbidden, InternalServerError, NotFound
from ..repositories.TrainingDayRepository import TrainingDayRepository
from ..models.trainingday import TrainingDay

class TrainingDayService(BaseService):

    def __init__(self, uow: UnitOfWork):
        super().__init__(uow)

    async def get_tr_day_with_access(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        tr_day_get_func: Callable[[Any], Awaitable],
        workout_get_func: Callable[[Any], Awaitable]
    ) -> TrainingDay:
        workout = await self._get_instance_with_access(
            identifier=workout_id,
            user_id=user_id,
            repo_get_func=workout_get_func
        )
        training_day = await self._get_existing_instance(
            identifier=day_id,
            repo_get_func=tr_day_get_func
        )
        if workout.id != training_day.workout_id:
            raise Forbidden()

        return training_day


    async def create_training_day(
        self,
        user_id: UUID,
        data: TrainingDayCreateDTO
    ) -> TrainingDay:
        async with self.uow as uow:
            await self._get_instance_with_access(
                identifier=data.workout_id,
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
            training_day = await self.get_tr_day_with_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id,
                tr_day_get_func=uow.trainingday.get_instance_by_id,
                workout_get_func=uow.workout.get_instance_by_id
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
            training_day = await self.get_tr_day_with_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id,
                tr_day_get_func=uow.trainingday.get_instance_by_id,
                workout_get_func=uow.workout.get_instance_by_id
            )
            await uow.trainingday.delete_by_id(id=day_id)

            return training_day
