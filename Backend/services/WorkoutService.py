import asyncio
from ..repositories.WorkoutRepository import WorkoutRepository
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.workout import DayExerciseResponse, DayExercisesScheme, TrainingDayResponse, TrainingDayScheme, WorkoutScheme, WorkoutResponse, WorkoutsFilter, UpdateDayExercise, UpdateWorkout, UpdateTrainingDays 
from ..models.workout import Workout
from ..models.trainingday import TrainingDay
from ..models.dayexercise import DayExercise
from ..utils.decorators import cache
from ..utils.validators import NotFound, DataNotModified
from datetime import timedelta
from uuid import UUID

class WorkoutService:

    def __init__(self, db: AsyncSession, redis: Redis):
        self.workoutrepo = WorkoutRepository(db=db)
        self.redis = redis

    async def create_workout_with_schedule(self, workout_schem: WorkoutScheme) -> WorkoutResponse:
        workout = Workout(
            user_id = workout_schem.user_id,
            name=workout_schem.name,
            description=workout_schem.description,
        )

        if workout_schem.training_days:
            for tr_day in workout_schem.training_days:
                training_day = TrainingDay(
                    name=tr_day.name,
                    day_order=tr_day.day_order,
                )

                if tr_day.day_exercises:
                    for day_ex in tr_day.day_exercises:
                        day_exercise = DayExercise(
                            exercise_id=day_ex.exercise_id,
                            exercise_order=day_ex.exercise_order,
                            sets=day_ex.sets,
                            reps=day_ex.reps
                        )
                        training_day.day_exercises.append(day_exercise)

                workout.training_days.append(training_day)
                
        workout_saved = await self.workoutrepo.create_instance(instance=workout)
        return await self.get_workout(workout_id=workout_saved.workout_id)

    async def create_training_day(self,
        workout_id: int,
        training_day_scheme: TrainingDayScheme
    ) -> WorkoutResponse:
        training_day = TrainingDay(
            workout_id=workout_id,
            name=training_day_scheme.name,
            day_order=training_day_scheme.day_order
        ) 

        if training_day_scheme.day_exercises:
            for day_ex in training_day_scheme.day_exercises:
                day_exercise = DayExercise(
                    exercise_id=day_ex.exercise_id,
                    exercise_order=day_ex.exercise_order,
                    sets=day_ex.sets,
                    reps=day_ex.reps
                )
                training_day.day_exercises.append(day_exercise)
            
        await self.workoutrepo.create_instance(training_day)
        await self.redis.delete(f"workout:{workout_id}")

        return await self.get_workout(workout_id=workout_id)

    async def create_day_exercise(self,
        workout_id: int,
        training_day_id: int,
        day_exercise_scheme: DayExercisesScheme
    ) -> WorkoutResponse:
        day_exercise = DayExercise(
            day_id=training_day_id,
            exercise_id=day_exercise_scheme.exercise_id,
            exercise_order=day_exercise_scheme.exercise_order,
            sets=day_exercise_scheme.sets,
            reps=day_exercise_scheme.reps
        )

        await self.workoutrepo.create_instance(day_exercise)
        await self.redis.delete(f"workout:{workout_id}")

        return await self.get_workout(workout_id=workout_id)
    
    @cache(expire=timedelta(hours=12), response_model=WorkoutResponse, prefix="workout")
    async def get_workout(self, workout_id: int) -> WorkoutResponse:
        workout = await self._get_workout_or_raise(workout_id=workout_id)
        return WorkoutResponse.model_validate(workout)
    
    async def get_all_workouts(self, 
        filter: WorkoutsFilter,
        user_id: UUID|None = None
    ) -> list[WorkoutResponse]:
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

    async def update_day_exercise(self,
        workout_id: int,
        data: list[UpdateDayExercise]
    ) -> WorkoutResponse:
        result = await self.workoutrepo.update_day_exercise([day.model_dump() for day in data])

        if result == 0:
            raise DataNotModified() 

        await self.redis.delete(f"workout:{workout_id}")

        updated_day_exercises_in_workout = await self.get_workout(workout_id=workout_id)
        return WorkoutResponse.model_validate(updated_day_exercises_in_workout)

    async def update_workout(self,
        workout_id: int,
        workout_update_data: UpdateWorkout
    ) -> WorkoutResponse:
        result = await self.workoutrepo.update_workout(
            workout_id=workout_id,
            workout_update_data=workout_update_data.model_dump()
        )

        if result == 0:
            raise DataNotModified()

        await self.redis.delete(f"workout:{workout_id}")

        updated_workout = await self.get_workout(workout_id=workout_id)
        return WorkoutResponse.model_validate(updated_workout)

    async def update_training_days(self,
        workout_id: int,
        training_day_id: int,
        training_day_update_data: UpdateTrainingDays
    ) -> WorkoutResponse:
        result = await self.workoutrepo.update_training_day(
            training_day_id=training_day_id,
            training_day_update_data=training_day_update_data.model_dump()
        )

        if result == 0:
            raise DataNotModified()

        await self.redis.delete(f"workout:{workout_id}")

        updated_training_day_in_workout = await self.get_workout(workout_id=workout_id)
        return WorkoutResponse.model_validate(updated_training_day_in_workout)

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
    
    
