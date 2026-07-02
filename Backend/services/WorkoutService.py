import asyncio
from ..schemas.workout import WorkoutCreate, DayExerciseCreate, TrainingDayCreate, WorkoutGetAllFilter, WorkoutMuscleRateResult, WorkoutResponse, WorkoutUpdate, TrainingDayUpdate, DayExerciseUpdate
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
                self._create_training_day(
                    data=tr_day,
                    workout=workout
                )
        
        created_workout = await self.workoutrepo.create_record_template(
            instance=workout
        )
        return created_workout

    @invalidate_cache(prefix="workout")
    async def create_training_day(self,
        workout_id: int,
        data: TrainingDayCreate
    ):
        training_day = self._create_training_day(
            data=data,
            workout_id=workout_id
        )
        created_training_day = await self.workoutrepo.create_record_template(
            instance=training_day
        )
        return created_training_day

    @staticmethod
    def _create_training_day(
        data: TrainingDayCreate,
        workout: Workout | None = None,
        workout_id: int | None = None
    ) -> TrainingDay:
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
        data: DayExerciseCreate
    ):
        day_exercise = DayExercise(
            day_id=training_day_id,
            exercise_id=data.exercise_id,
            exercise_order=data.exercise_order,
            sets=data.sets,
            reps=data.reps
        )

        await self.workoutrepo.create_instance(day_exercise)

        return await self.workoutrepo.get_workout(workout_id=workout_id)
    
    @cache(ttl=timedelta(hours=12), prefix="workout", schema=WorkoutResponse)
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
        training_day_id: int,
        exercise_id: int,
        data: DayExerciseUpdate
    ):
        rowcount = await self.workoutrepo.update_day_exercise(
            training_day_id=training_day_id,
            exercise_id=exercise_id,
            data=data.model_dump(exclude_unset=True)
        )

        return await self._get_updated_workout(
            workout_id=workout_id,
            rowcount=rowcount
        )

    @invalidate_cache(prefix="workout")
    async def update_workout(self,
        workout_id: int,
        data: WorkoutUpdate
    ):
        rowcount = await self.workoutrepo.update_workout(
            workout_id=workout_id,
            data=data.model_dump(exclude_unset=True)
        )
        return await self._get_updated_workout(
            workout_id=workout_id,
            rowcount=rowcount
        )

    @invalidate_cache(prefix="workout")
    async def update_training_day(self,
        workout_id: int,
        training_day_id: int,
        data: TrainingDayUpdate
    ):
        rowcount = await self.workoutrepo.update_training_day(
            training_day_id=training_day_id,
            data=data.model_dump(exclude_unset=True)
        )
        return await self._get_updated_workout(
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

    @invalidate_cache(prefix="workout")
    async def delete_training_day(self,
        workout_id: int,
        training_day_id: int
    ) -> None:
        result = await self.workoutrepo.delete_training_day(training_day_id=training_day_id)
        if result == 0:
            raise NotFound()

    @invalidate_cache(prefix="workout")
    async def delete_day_exercise(self,
        workout_id: int,
        training_day_id: int,
        exercise_id: int
    ) -> None: 
        result = await self.workoutrepo.delete_day_exercise(
            training_day_id=training_day_id,
            exercise_id=exercise_id
        )

        if result == 0:
            raise NotFound()

    async def calculate_rate_balance(self,
        workout_id: int
    ):
        muscles_name = await self.workoutrepo.get_all_muscles()
        all_muscles = {muscle: 0.0 for muscle in muscles_name}

        activated_muscles_json = await self.workoutrepo.get_all_trainted_muscles_in_workout(workout_id=workout_id)
        for muscle_json in activated_muscles_json:
            for name, coefficient in muscle_json.items():
                all_muscles[name] += coefficient

        result = [
            WorkoutMuscleRateResult(
                muscle=name,
                score=coefficient,
                status=self._calculate_status(coefficient)
            )
            for name, coefficient in all_muscles.items()
        ]
        return result

    @staticmethod
    def _calculate_status(coefficient: float) -> str:
        if coefficient < 1.0:
            return "under_trained"
        elif coefficient > 2.0:
            return "over_trained"
        else:
            return "normal"

    async def _get_workout_or_raise(self, workout_id: int) -> Workout:
        workout = await self.workoutrepo.get_workout(workout_id=workout_id)
        if not workout:
            raise NotFound()
        return workout
    
    
