from Backend.trainings.domain.exceptions.workout_exceptions import (
    Forbidden,
    WorkoutNotFound,
)
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository

from uuid import UUID


class DeleteWorkoutUseCase:
    def __init__(self, workout_repo: IWorkoutRepository) -> None:
        self.workout_repo = workout_repo

    async def __cal__(self, user_id: UUID, workout_id: int) -> None:
        workout = await self.workout_repo.get(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if workout.user_id != user_id:
            raise Forbidden()

        await self.workout_repo.delete(workout)
