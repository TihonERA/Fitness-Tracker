from typing import Protocol

from Backend.trainings.domain.workout_model import Workout


class WorkoutReaderPort(Protocol):
    async def get(self, id: int) -> Workout: ...
