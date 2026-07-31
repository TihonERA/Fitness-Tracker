import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from Backend.models.workout import Workout
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayUpdate
from Backend.services.DayExerciseService import DayExerciseService
from Backend.utils.decorators import invalidate_cache
from ..utils.validators import InternalServerError, NotFound
from ..repositories.TrainingDayRepository import TrainingDayRepository
from ..models.trainingday import TrainingDay

class TrainingDayService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis
        self.trdayrepo = TrainingDayRepository(session=session)
        self.workoutrepo = WorkoutRepository(session=session)

    async def get_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ) -> TrainingDay:
        training_day = await self.trdayrepo.get_training_day_and_check_access(
            user_id=user_id,
            workout_id=workout_id,
            day_id=day_id
        )
        if training_day is None:
            raise NotFound()

        return training_day

    @invalidate_cache(column=Workout.workout_id)
    async def create_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        data: TrainingDayCreate
    ) -> TrainingDay:
        workout = await self.workoutrepo.get_workout_and_check_access(
            user_id=user_id,
            workout_id=workout_id
        )
        if workout is None:
            raise NotFound()

        return await self.trdayrepo.create_instance(
            data={**data.model_dump(), "workout_id": workout_id}
        )

    @invalidate_cache(column=Workout.workout_id)
    async def update_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int,
        data: TrainingDayUpdate
    ):
        workout, training_day = await asyncio.gather(
            self.workoutrepo.get_workout_and_check_access(
                user_id=user_id,
                workout_id=workout_id
            ),
            self.trdayrepo.get_training_day_for_update(
                day_id=day_id
            )
        )
        if (
            training_day is None
            or workout is None
            or training_day.workout_id != workout.workout_id
        ):
            raise NotFound()

        try:
            result = await self.trdayrepo.update_instance(
                instance=training_day,
                data=data.model_dump(exclude_unset=True)
            )
        except AttributeError as e:
            raise InternalServerError(
                detail=f"Table: {training_day.__tablename__} dont have attribute {e.name}, that was declared at a pydantic model"
            )


        return result

    @invalidate_cache(column=Workout.workout_id)
    async def delete_training_day(
        self,
        user_id: UUID,
        workout_id: int,
        day_id: int
    ):
        workout, training_day = await asyncio.gather(
            self.workoutrepo.get_workout_and_check_access(
                user_id=user_id,
                workout_id=workout_id
            ),
            self.trdayrepo.get_training_day_for_update(
                day_id=day_id
            )
        )
        if (
            workout is None
            or training_day is None
            or workout.workout_id != training_day.workout_id
        ):
            raise NotFound()

        await self.trdayrepo.delete_training_day(
            day_id=day_id
        )

        return training_day
