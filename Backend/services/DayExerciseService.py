from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.dayexercise import DayExercise
from Backend.models.workout import Workout
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.workout import DayExerciseCreate, DayExerciseUpdate
from Backend.utils.decorators import invalidate_cache
from ..repositories.DayExerciseRepository import DayExerciseRepository
from ..utils.validators import NotFound


class DayExerciseService:
    
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis
        self.dayexerepo = DayExerciseRepository(session=session)
        self.workoutrepo = WorkoutRepository(session=session)

    @invalidate_cache(column=Workout.workout_id)
    async def create_day_exercise(
        self,
        workout_id: int,
        day_id: int,
        data: DayExerciseCreate
    ):
        day_exercise = DayExercise(
            day_id=day_id,
            exercise_id=data.exercise_id,
            workout_id=workout_id,
            exercise_order=data.exercise_order,
            sets=data.sets,
            reps=data.reps
        )

        return await self.dayexerepo.create_instance(instance=day_exercise)

    @invalidate_cache(column=Workout.workout_id)
    async def update_day_exercise(
        self,
        day_id: int,
        exercise_id: int,
        data: DayExerciseUpdate
    ):
        result = await self.dayexerepo.update_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id,
            data=data.model_dump(exclude_unset=True)
        )
        if result is None:
            raise NotFound()

        return result

    @invalidate_cache(column=Workout.workout_id)
    async def delete_day_exercise(
        self,
        workout_id: int,
        day_id: int,
        exercise_id: int
    ):
        workout  =  await self.workoutrepo.get_workout(workout_id=workout_id)
        if workout is None:
            raise NotFound()
        
        tr_day = next((d for d in workout.training_days if d.day_id == day_id), None)
        if tr_day is None:
            raise NotFound()

        ex_day = next((e for e in tr_day.day_exercises if e.exercise_id == exercise_id), None)
        if ex_day is None:
            raise NotFound()

        await self.dayexerepo.delete_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        return ex_day
