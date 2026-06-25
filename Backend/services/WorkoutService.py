import asyncio
from ..schemas.workout import WorkoutCreate, DayExerciseCreate, TrainingDayCreate, WorkoutGetAllFilter, WorkoutUpdate, TrainingDayUpdate, DayExerciseUpdate
from ..repositories.WorkoutRepository import WorkoutRepository
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from ..models.trainingday import TrainingDay
from ..models.dayexercise import DayExercise
from ..utils.decorators import cache, invalidate_cache
from ..utils.validators import NotFound
from datetime import timedelta
from uuid import UUID

class WorkoutService:

    def __init__(self, db: AsyncSession, redis: Redis):
        self.workoutrepo = WorkoutRepository(db=db)
        self.redis = redis

    async def create_workout_with_schedule(self,
        data: WorkoutCreate
    ):
        workout = Workout(
            user_id = data.user_id,
            name=data.name,
            description=data.description,
        )

        if data.training_days:
            for tr_day in data.training_days:
                tr_day_data = TrainingDayCreate(
                   name=tr_day.name,
                   day_order=tr_day.day_order
                )
                self._create_training_day(
                    data=tr_day_data,
                    workout=workout
                )

        return self.workoutrepo.create_instance(instance=workout)

    @invalidate_cache(prefix="workout")
    async def create_training_day(self,
        workout_id: int,
        data: TrainingDayCreate
    ):
        training_day = self._create_training_day(
            data=data,
            workout_id=workout_id
        )
        await self.workoutrepo.create_instance(instance=training_day)

        return await self.workoutrepo.get_workout(workout_id=workout_id)

    def _create_training_day(self,
        data: TrainingDayCreate,
        workout: Workout | None = None,
        workout_id: int | None = None
    ):
        training_day = TrainingDay(
            name=data.name,
            day_order=data.day_order
        ) 

        if workout:
            workout.training_days.append(training_day)
        elif workout_id:
            training_day.workout_id = workout_id

        if data.day_exercises:
            for day_ex in data.day_exercises:
                day_exercise = DayExercise(
                    exercise_id=day_ex.exercise_id,
                    exercise_order=day_ex.exercise_order,
                    sets=day_ex.sets,
                    reps=day_ex.reps
                )
                training_day.day_exercises.append(day_exercise)

        return training_day
      
    @invalidate_cache(prefix="workout")
    async def create_day_exercise(self,
        workout_id: int,
        training_day_id: int,
        day_exercise_scheme: DayExerciseCreate
    ):
        day_exercise = DayExercise(
            day_id=training_day_id,
            exercise_id=day_exercise_scheme.exercise_id,
            exercise_order=day_exercise_scheme.exercise_order,
            sets=day_exercise_scheme.sets,
            reps=day_exercise_scheme.reps
        )

        await self.workoutrepo.create_instance(day_exercise)

        return await self.workoutrepo.get_workout(workout_id=workout_id)
    
    @cache(ttl=timedelta(hours=12), prefix="workout")
    async def get_workout(self, workout_id: int):
        return await self._get_workout_or_raise(workout_id=workout_id)
    
    async def get_all_workouts(self, 
        filter: WorkoutGetAllFilter,
        user_id: UUID|None = None
    ):
        workouts_id = await self.workoutrepo.get_all_workouts(
            skip=filter.skip,
            limit=filter.limit,
            user_id=user_id,
            public=filter.public
        )

        if not workouts_id:
            return []
        
        tasks = [self.get_workout(workout_id) for workout_id in workouts_id]

        workouts = await asyncio.gather(*tasks)
        return list(workouts)

    @invalidate_cache(prefix="workout")
    async def update_day_exercise(self,
        workout_id: int,
        data: list[DayExerciseUpdate]
    ):
        rowcount = await self.workoutrepo.update_day_exercise(
            [day.model_dump() for day in data]
        )

        return await self._get_updated_workout(
            workout_id=workout_id,
            rowcount=rowcount
        )

    @invalidate_cache(prefix="workout")
    async def update_workout(self,
        workout_id: int,
        workout_update_data: WorkoutUpdate
    ):
        rowcount = await self.workoutrepo.update_workout(
            workout_id=workout_id,
            workout_update_data=workout_update_data.model_dump()
        )
        return await self._get_updated_workout(
            workout_id=workout_id,
            rowcount=rowcount
        )

    @invalidate_cache(prefix="workout")
    async def update_training_days(self,
        workout_id: int,
        training_day_id: int,
        training_day_update_data: TrainingDayUpdate
    ):
        rowcount = await self.workoutrepo.update_training_day(
            training_day_id=training_day_id,
            training_day_update_data=training_day_update_data.model_dump()
        )
        return self._get_updated_workout(
            workout_id=workout_id,
            rowcount=rowcount
        )

    async def _get_updated_workout(self,
        workout_id: int,
        rowcount: int
    ):
        if rowcount == 0:
            raise NotFound()

        return await self.workoutrepo.get_workout(workout_id=workout_id)
        
    @invalidate_cache(prefix="workout")
    async def delete_workout(self,
        workout_id: int
    ) -> None:
        result = await self.workoutrepo.delete_workout(workout_id=workout_id)
        if result == 0:
            raise NotFound() 

    async def delete_training_day(self,
        training_day_id: int
    ) -> None:
        result = await self.workoutrepo.delete_training_day(training_day_id=training_day_id)
        if result == 0:
            raise NotFound()

    async def delete_day_exercise(self,
        day_id: int,
        exercise_id: int
    ) -> None: 
        result = await self.workoutrepo.delete_day_exercise(
            day_id=day_id,
            exercise_id=exercise_id
        )

        if result == 0:
            raise NotFound()

    async def _get_workout_or_raise(self, workout_id: int) -> Workout:
        workout = await self.workoutrepo.get_workout(workout_id=workout_id)
        if not workout:
            raise NotFound()
        return workout
    
    
