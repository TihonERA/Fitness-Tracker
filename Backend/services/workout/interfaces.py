from abc import ABC, abstractmethod

from Backend.models.workout import Workout

from Backend.schemas.workout import WorkoutGetAllFilterDTO

from typing import Sequence


class WorkoutRepositoryInterface(ABC):
    @abstractmethod
    async def get_workout(self, workout_id: int) -> Workout | None:
        pass

    @abstractmethod
    async def get_all_workouts(self, data: WorkoutGetAllFilterDTO) -> Sequence[Workout]:
        pass
