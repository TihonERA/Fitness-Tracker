from abc import ABC, abstractmethod

from Backend.models.workout import Workout

from Backend.schemas.workout import WorkoutGetAllFilterDTO

from Backend.core.interfaces.uow import BaseUOWInterface

from Backend.infrastructure.WorkoutRepository import WorkoutRepository

from typing import Sequence


class WorkoutRepositoryInterface(ABC):
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
