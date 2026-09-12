from abc import ABC, abstractmethod
from uuid import UUID

from pydantic.main import ModelT
from Backend.schemas.workout import WorkoutCreate, WorkoutGetAllFilter, WorkoutUpdate

from Backend.core.interfaces.base_repository_interfaces import (
    BaseCreateRepositoryInterface,
    BaseDeleteRepositoryInterface,
    BaseReadAllRepositoryInterface,
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.services.base_service_components.interfaces import (
    DeleteAuthorizedServiceInterface,
    ReadAllServiceInterface,
    ReadRelationAuthorizedServiceInterface,
    RegisterServiceInterface,
    UpdateAuthorizedServiceInterface,
)

from Backend.models.workout import Workout

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Sequence, TypeGuard


class WorkoutRepositoryInterface(
    BaseCreateRepositoryInterface[Workout],
    BaseReadRelationRepositoryInterface[Workout],
    BaseReadAllRepositoryInterface[Workout, WorkoutGetAllFilter],
    BaseUpdateRepositoryInterface[Workout],
    BaseDeleteRepositoryInterface[Workout],
):
    pass


class WorkoutUOWInterface(BaseUOWInterface):
    @property
    @abstractmethod
    def workout(self) -> WorkoutRepositoryInterface:
        pass


class WorkoutRegisterServiceInterface(RegisterServiceInterface[Workout, WorkoutCreate]):
    pass


class WorkoutReadRelationAuthServiceInterface(
    ReadRelationAuthorizedServiceInterface[Workout]
):
    @abstractmethod
    async def fetch_authorized(self, *, id: int, user_id: UUID) -> Workout:
        pass


class WorkoutReadAllServiceInterface(
    ReadAllServiceInterface[Workout, WorkoutGetAllFilter]
):
    pass


class WorkoutUpdateAuthServiceInterface(
    UpdateAuthorizedServiceInterface[Workout, WorkoutUpdate]
):
    pass


class WorkoutDeleteAuthServiceInterface(DeleteAuthorizedServiceInterface[Workout]):
    pass
