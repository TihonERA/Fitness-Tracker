from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository

from uuid import UUID


class DeleteWorkoutUseCase:
    def __init__(self, workout_repo: IWorkoutRepository) -> None:
        self.workout_repo = workout_repo

    async def __call__(self, user_id: UUID, workout_id: int) -> None:
        workout = await self.workout_repo.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        workout.ensure_ownership(user_id)

        await self.workout_repo.delete(workout_id)
