from Backend.trainings.application.dto.workout import UpdateWorkoutCommand
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutNotFound,
)
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository
from Backend.trainings.domain.workout_model import Workout


class UpdateWorkoutUseCase:
    def __init__(self, workout_repo: IWorkoutRepository) -> None:
        self.workout_repo = workout_repo

    async def __call__(self, command: UpdateWorkoutCommand) -> Workout:
        workout = await self.workout_repo.get(command.workout_id)

        if workout is None:
            raise WorkoutNotFound(command.workout_id)

        workout.ensure_ownership(command.user_id)

        workout.update(
            name=command.name, description=command.description, public=command.public
        )

        return await self.workout_repo.update(workout)
