from typing import Protocol
from uuid import UUID

from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)

from Backend.trainings.domain.workout_model import Workout


class WorkoutReader(Protocol):
    async def get_loaded(self, id: int) -> Workout | None: ...


class GetLoadedWorkoutUseCase:
    def __init__(self, workout_repo: WorkoutReader) -> None:
        self.workout_repo = workout_repo

    async def __call__(self, user_id: UUID, workout_id: int) -> Workout:
        workout = await self.workout_repo.get_loaded(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if not workout.public:
            workout.ensure_ownership(user_id)

        return workout
