from abc import ABC, abstractmethod

from Backend.core.interfaces.base_repository_interfaces import (
    BaseCreateRepositoryInterface,
    BaseDeleteRepositoryInterface,
    BaseReadRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.models.workout import Workout

from Backend.schemas.workout import WorkoutGetAllFilterDTO

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Sequence


class WorkoutRepositoryInterface(
    BaseCreateRepositoryInterface[Workout],
    BaseReadRepositoryInterface[Workout],
    BaseUpdateRepositoryInterface[Workout],
    BaseDeleteRepositoryInterface[Workout],
):
    @abstractmethod
    async def get_loaded(self, id: int) -> Workout | None:
        pass

    @abstractmethod
    async def get_all(self, data: WorkoutGetAllFilterDTO) -> Sequence[Workout]:
        pass


class WorkoutUOWInterface(BaseUOWInterface):
    @property
    @abstractmethod
    def workout(self) -> WorkoutRepositoryInterface:
        pass
