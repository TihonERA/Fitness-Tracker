import asyncio
from Backend.services.TrainingDayService import TrainingDayService
from ..schemas.workout import WorkoutCreate, WorkoutGetAllFilter, WorkoutResponse, WorkoutUpdate
from ..repositories.WorkoutRepository import WorkoutRepository
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from ..utils.decorators import cache, invalidate_cache
from ..utils.validators import NotFound
from datetime import timedelta
from uuid import UUID

class WorkoutService:

    def __init__(self, session: AsyncSession, redis: Redis):
        self.workoutrepo = WorkoutRepository(session=session)
        self.trdayservice = TrainingDayService(session=session, redis=redis)
        self.redis = redis

    async def create_workout_with_schedule(self,
        data: WorkoutCreate
    ):
        workout = Workout(
            user_id = data.user_id,
            name=data.name,
            description=data.description,
        )

        workout = await self.workoutrepo.create_instance(instance = workout)

        for tr_day in data.training_days:
            await self.trdayservice.create_training_day(
                workout_id=workout.workout_id,
                data=tr_day
            )

        return await self.workoutrepo.get_workout(workout_id=workout.workout_id)

    @cache(ttl=timedelta(hours=12), column=Workout.workout_id, schema=WorkoutResponse)
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

    @invalidate_cache(column=Workout.workout_id)
    async def update_workout(
        self,
        workout_id: int,
        data: WorkoutUpdate
    ):
        rowcount = await self.workoutrepo.update_workout(
            workout_id=workout_id,
            data=data.model_dump(exclude_unset=True)
        )
        if rowcount == 0:
            raise NotFound()
        
        return await self.workoutrepo.get_workout(workout_id=workout_id) 
       
    @invalidate_cache(column=Workout.workout_id)
    async def delete_workout(
        self,
        workout_id: int
    ) -> Workout:
        workout = await self.workoutrepo.get_workout(workout_id=workout_id)
        if workout is None:
            raise NotFound()

        await self.workoutrepo.delete_workout(workout_id=workout_id)

        return workout

    async def get_muscles_distribution_list(self,
        workout_id: int
    ):
        all_muscle_with_coef = await self._get_all_muscles_coef(
            workout_id=workout_id
        )
        
        result = [
            {
                "muscle": name,
                "score": round(coefficient, 2),
                "status": self._calculate_status(round(coefficient, 2))
            }
            for name, coefficient in all_muscle_with_coef.items()
        ]
        return result

    async def _get_all_muscles_coef(
        self,
        workout_id: int
    ) -> dict[str, float]:
        muscles_name = await self.workoutrepo.get_all_muscles()
        all_muscle_with_coef = {muscle: 0.0 for muscle in muscles_name}

        activated_muscles_json = await self.workoutrepo.get_all_trainted_muscles_in_workout(workout_id=workout_id)
        if activated_muscles_json == []:
            raise NotFound()

        for muscle_json in activated_muscles_json:
            for name, coefficient in muscle_json.items():
                all_muscle_with_coef[name] += coefficient

        return all_muscle_with_coef

    @staticmethod
    def _calculate_status(coefficient: float) -> str:
        if coefficient < 1.0:
            return "under_trained"
        elif coefficient > 2.0:
            return "over_trained"
        else:
            return "normal"

    async def get_muscles_balance(self,
        workout_id: int
    ):
        all_muscle_with_coef = await self._get_all_muscles_coef(
            workout_id=workout_id
        )

        all_muscles_with_antagonists = await self.workoutrepo.get_all_muscles_antagonists()

        disbalance_muscles = []
        for muscle, antagonist in all_muscles_with_antagonists:
            difference = self._calculate_difference(
                all_muscle_with_coef[muscle],
                all_muscle_with_coef[antagonist]
            )
            if not (0.7 <= difference <= 1.3):
                muscle_status = self._calculate_muscles_antagonist_ratio(
                    difference=difference
                )
                disbalance_muscles.append(
                    {
                        "muscle": muscle,
                        "antagonist": antagonist,
                        "detail": f"{muscle} is {muscle_status} compared to {antagonist}"
                    }
                )

        return disbalance_muscles

    @staticmethod
    def _calculate_difference(muscle_one: float, muscle_two: float):
        try:
            difference = round(muscle_one / muscle_two, 1)
        except ZeroDivisionError:
            difference = 99.0

        return difference

    @staticmethod
    def _calculate_muscles_antagonist_ratio(
        difference: float
    ):
        if difference < 0.7:
            return "under_trained" 
        elif difference > 1.3:
            return "over_trained"

    async def _get_workout_or_raise(self, workout_id: int) -> Workout:
        workout = await self.workoutrepo.get_workout(workout_id=workout_id)
        if not workout:
            raise NotFound()
        return workout
    
    
