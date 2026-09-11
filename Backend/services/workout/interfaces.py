from abc import ABC, abstractmethod

from Backend.core.interfaces.base_repository_interfaces import (
    BaseCreateRepositoryInterface,
    BaseDeleteRepositoryInterface,
    BaseReadAllRepositoryInterface,
    BaseReadRelationRepositoryInterface,
    BaseReadRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.models.workout import Workout

from Backend.schemas.workout import WorkoutGetAllFilterDTO

from Backend.core.interfaces.uow import BaseUOWInterface

from typing import Sequence


class WorkoutRepositoryInterface(
    BaseCreateRepositoryInterface[Workout],
    BaseReadRelationRepositoryInterface[Workout],
    BaseReadAllRepositoryInterface[Workout, WorkoutGetAllFilterDTO],
    BaseUpdateRepositoryInterface[Workout],
    BaseDeleteRepositoryInterface[Workout],
):
    pass


class WorkoutUOWInterface(BaseUOWInterface):
    @property
    @abstractmethod
    def workout(self) -> WorkoutRepositoryInterface:
        pass
