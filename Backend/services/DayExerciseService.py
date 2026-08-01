import asyncio
from typing import Any
from uuid import UUID

from annotated_types import Not
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise
from Backend.models.workout import Workout
from Backend.repositories.TrainingDayRepository import TrainingDayRepository
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseUpdate
from Backend.utils.decorators import invalidate_cache
from Backend.utils.uow import UnitOfWork
from ..repositories.DayExerciseRepository import DayExerciseRepository
from ..utils.exceptions import InternalServerError, NotFound


class DayExerciseService:
    
    def __init__(self, uow: UnitOfWork, redis: Redis):
        self.uow = uow
        self.redis = redis
        self.dayexerepo = uow.dayexercise
        self.trdayrepo = uow.trainingday
        self.workoutrepo = uow.workout

    async def get_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ) -> DayExercise:
        day_exercise = await self.dayexerepo.get_day_exercise_and_check_access(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id,
            exercise_id=exercise_id
        )
        day_exercise, = self.check_if_instaces_is_none(day_exercise)

        return day_exercise

    @invalidate_cache(column=Workout.workout_id)
    async def create_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: DayExerciseCreate
    ):
        tr_day = await self.trdayrepo.get_training_day_and_check_access(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id
        )
        tr_day, = self.check_if_instaces_is_none(tr_day)

        return await self.dayexerepo.create_instance(
            data={**data.model_dump(), "day_id": day_id, "workout_id": workout_id}
        )

    @invalidate_cache(column=Workout.workout_id)
    async def update_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int,
        data: DayExerciseUpdate
    ):
        tr_day, day_exercise = await asyncio.gather(
            self.trdayrepo.get_training_day_and_check_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id
            ),
            self.dayexerepo.get_day_exercise_for_update(
                day_id=day_id,
                exercise_id=exercise_id
            )
        )

        tr_day, day_exercise = self.check_if_instaces_is_none(tr_day, day_exercise)

        try:
            result = await self.dayexerepo.update_instance(
                instance=day_exercise,
                data=data.model_dump(exclude_unset=True)
            )
        except AttributeError as e:
            raise InternalServerError(
                detail=f"Table: {day_exercise.__tablename__} dont have attribute {e.name}, that was declared at a pydantic model"
            )
        return result

    @invalidate_cache(column=Workout.workout_id)
    async def delete_day_exercise(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ):
        tr_day, ex_day = await asyncio.gather(
            self.trdayrepo.get_training_day_and_check_access(
                user_id=user_id,
                workout_id=workout_id,
                day_id=day_id
            ),
            self.dayexerepo.get_day_exercise_for_update(
                day_id=day_id,
                exercise_id=exercise_id
            )
        )

        tr_day, ex_day = self.check_if_instaces_is_none(tr_day, ex_day)

        await self.dayexerepo.delete_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        return ex_day
    
    @staticmethod
    def check_if_instaces_is_none(*args: Any) -> tuple[Any, ...]:
        for instance in args:
            if instance is None:
                raise NotFound()
        return args
