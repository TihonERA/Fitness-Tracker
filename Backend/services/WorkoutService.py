import asyncio
from Backend.services.BaseService import BaseService
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.uow import UnitOfWork
from ..schemas.workout import WorkoutCreate, WorkoutCreateDTO, WorkoutGetAllFilter, WorkoutResponse, WorkoutUpdate
from ..repositories.WorkoutRepository import WorkoutRepository
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workout import Workout
from ..utils.decorators import cache, invalidate_cache
from ..utils.exceptions import InternalServerError, NotFound
from datetime import timedelta
from uuid import UUID

class WorkoutService(BaseService):

    def __init__(self, uow: UnitOfWork, redis: Redis):
        super().__init__(uow=uow, redis=redis)
        
    async def create_workout(
        self,
        user_id: UUID,
        data: WorkoutCreate
    ):
        async with self.uow as uow:
            data_dto = WorkoutCreateDTO(
                **data.model_dump(),
                user_id=user_id
            )
            return await uow.workout.create_instance(
                data=data_dto
            )
            
    async def get_workout(
        self,
        workout_id: int,
        user_id: UUID  
    ) -> Workout:
        workout = await self._get_workout_or_raise(workout_id=workout_id)
        if workout.user_id != user_id:
            raise NotFound()

        return workout

    async def get_all_workouts(self, 
        filter: WorkoutGetAllFilter,
    ):
        workouts_id = await self.workoutrepo.get_all_workouts(
            skip=filter.skip,
            limit=filter.limit,
            user_id=filter.user_id,
            public=filter.public
        )

        if not workouts_id:
            return []
        
        tasks = [self._get_workout_or_raise(workout_id) for workout_id in workouts_id]

        workouts = await asyncio.gather(*tasks)
        return list(workouts)

    async def update_workout(
        self,
        user_id: UUID,
        workout_id: int,
        data: WorkoutUpdate
    ) -> Workout:
        workout = await self.workoutrepo.get_instance_for_update(
            id=workout_id,
        )
        workout, = self.check_if_instaces_is_none_returning_tuple(workout)

        if workout.user_id != user_id:
            raise NotFound()
        
        try:
            updated_workout = await self.workoutrepo.update_instance(
                instance=workout,
                data=data
            )
        except AttributeError as e:
            raise InternalServerError(
                detail=f"Table: {workout.__tablename__} dont have attribute {e.name}, that was declared at a pydantic model"
            )
        return updated_workout
       
    async def delete_workout(
        self,
        user_id: UUID,
        workout_id: int
    ) -> Workout:
        workout = await self.workoutrepo.get_instance_for_update(
            id=workout_id
        )
        workout, = self.check_if_instaces_is_none_returning_tuple(workout)

        if workout.user_id != user_id:
            raise NotFound()

        await self.workoutrepo.delete_by_id(id=workout_id)

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
    
    
