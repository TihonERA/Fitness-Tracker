import asyncio
from typing import Any
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise
from Backend.models.workout import Workout
from Backend.repositories.TrainingDayRepository import TrainingDayRepository
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseCreateDTO 
from Backend.services.BaseService import BaseService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.uow import UnitOfWork
from ..repositories.DayExerciseRepository import DayExerciseRepository
from ..utils.exceptions import Forbidden, InternalServerError, NotFound


class DayExerciseService(BaseService):
    
    def __init__(self, uow: UnitOfWork):
        self.tr_day_service = TrainingDayService(uow=uow)
        super().__init__(uow)

    async def create_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: DayExerciseCreateDTO
    ):
        async with self.uow as uow:
            await self.tr_day_service.get_tr_day_with_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id,
                tr_day_get_func=uow.trainingday.get_instance_by_id,
                workout_get_func=uow.workout.get_instance_by_id
            )
                
            return await uow.dayexercise.create_instance(
                data=data
            )

    async def delete_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ):
        async with self.uow as uow:
            training_day = await self.tr_day_service.get_tr_day_with_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id,
                tr_day_get_func=uow.trainingday.get_instance_by_id,
                workout_get_func=uow.workout.get_instance_by_id
            )
            day_exercise = await uow.dayexercise.get_day_exercise(
                day_id=day_id,
                exercise_id=exercise_id
            )
            if day_exercise is None:
                raise NotFound()

            if training_day.id != day_exercise.day_id:
                raise Forbidden()

            await uow.dayexercise.delete_day_exercise(
                day_id=day_id,
                exercise_id=exercise_id
            )

            return day_exercise
