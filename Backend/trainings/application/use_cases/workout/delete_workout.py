from typing import Protocol

from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)

from uuid import UUID

from Backend.trainings.domain.workout_model import Workout


class WorkoutDeleter(Protocol):
    async def get(self, id: int) -> Workout | None: ...

    async def delete(self, id: int) -> None: ...


class DeleteWorkoutUseCase:
    def __init__(self, workout_repo: WorkoutDeleter) -> None:
        self.workout_repo = workout_repo

    async def __call__(self, user_id: UUID, workout_id: int) -> None:
        workout = await self.workout_repo.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        workout.ensure_ownership(user_id)

        await self.workout_repo.delete(workout_id)
