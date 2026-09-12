from typing import Sequence

from Backend.services.base_service_components.interfaces import (
    DeleteAuthorizedServiceInterface,
    ReadAllServiceInterface,
    ReadRelationAuthorizedServiceInterface,
    RegisterServiceInterface,
    UpdateAuthorizedServiceInterface,
)
from Backend.services.workout.interfaces import (
    WorkoutRepositoryInterface,
    WorkoutUOWInterface,
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


class WorkoutService:
    def __init__(
        self,
        uow: WorkoutUOWInterface,
        create_service: RegisterServiceInterface[Workout, WorkoutCreate],
        read_relation_auth_service: ReadRelationAuthorizedServiceInterface[Workout],
        read_all_service: ReadAllServiceInterface[Workout, WorkoutGetAllFilter],
        update_auth_service: UpdateAuthorizedServiceInterface[Workout, WorkoutUpdate],
        delete_auth_service: DeleteAuthorizedServiceInterface[Workout],
    ) -> None:
        self.uow = uow
        self.create_service = create_service
        self.read_relation_auth_service = read_relation_auth_service
        self.read_all_service = read_all_service
        self.update_auth_service = update_auth_service
        self.delete_auth_service = delete_auth_service

    @property
    def repository(self) -> WorkoutRepositoryInterface:
        return self.uow.workout

    async def create(self, user_id: UUID, data: WorkoutCreate) -> Workout:
        async with self.uow:
            return await self.create_service.create(user_id, data)

    async def get_loaded(self, workout_id: int, user_id: UUID) -> Workout:
        async with self.uow:
            return await self.read_relation_auth_service.fetch_authorized(
                workout_id, user_id
            )

    async def get_all_workouts(
        self, data: WorkoutGetAllFilter, user_id: UUID
    ) -> Sequence[Workout]:
        async with self.uow:
            return await self.read_all_service.fetch_all(user_id, data)

    async def update_workout(
        self, workout_id: int, user_id: UUID, data: WorkoutUpdate
    ) -> Workout:
        async with self.uow:
            return await self.update_auth_service.update(
                data=data, id=workout_id, user_id=user_id
            )

    async def delete_workout(self, workout_id: int, user_id: UUID) -> None:
        async with self.uow:
            await self.delete_auth_service.delete(id=workout_id, user_id=user_id)
