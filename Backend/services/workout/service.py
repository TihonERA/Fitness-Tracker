from typing import Sequence

from Backend.services.BaseService import BaseService

from Backend.utils.uow import UnitOfWork
from Backend.utils.exceptions import (
    Forbidden,
    InternalServerError,
    NotFound,
    DBErrorHandler,
)

from Backend.schemas.workout import (
    WorkoutCreate,
    WorkoutCreateDTO,
    WorkoutGetAllFilter,
    WorkoutGetAllFilterDTO,
    WorkoutRelationsResponse,
    WorkoutResponse,
    WorkoutUpdate,
)

from Backend.models.workout import Workout

from uuid import UUID


class WorkoutService(BaseService[Workout]):

    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow=uow)

    async def create_workout(self, user_id: UUID, data: WorkoutCreate) -> Workout:
        async with self.uow as uow:
            data_dto = WorkoutCreateDTO(**data.model_dump(), user_id=user_id)
            return await uow.workout.create_instance(data_dto)

    async def get_loaded_workout(
        self, workout_id: int, user_id: UUID
    ) -> Workout | bytes | str:
        async with self.uow as uow:
            return await self._get_instance_with_access(
                identifier=workout_id,
                user_id=user_id,
                repo_get_func=uow.workout.get_workout,
            )

    async def get_all_workouts(
        self,
        data: WorkoutGetAllFilterDTO,
    ) -> Sequence[Workout]:
        async with self.uow as uow:
            return await self.get_all_instances(
                data=data, repo_get_all_func=uow.workout.get_all_workouts
            )

    async def update_workout(
        self, user_id: UUID, workout_id: int, data: WorkoutUpdate
    ) -> Workout:
        async with self.uow as uow:
            return await self.update_instance_with_access(
                user_id=user_id, id=workout_id, data=data, repo=uow.workout
            )

    async def delete_workout(self, user_id: UUID, workout_id: int) -> Workout:
        async with self.uow as uow:
            return await self.delete_instance_with_access(
                user_id=user_id, id=workout_id, repo=uow.workout
            )
