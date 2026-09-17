from abc import ABC, abstractmethod

from Backend.trainings.domain.workout_model import Workout


class IWorkoutRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Workout | None: ...

    @abstractmethod
    async def get_loaded(self, id: int) -> Workout | None: ...

    @abstractmethod
    async def create(self, workout: Workout) -> Workout: ...

    @abstractmethod
    async def update(self, workout: Workout) -> Workout: ...

    @abstractmethod
    async def delete(self, workout: Workout) -> None: ...
