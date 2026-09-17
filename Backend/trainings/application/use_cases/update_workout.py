from Backend.trainings.application.dto.workout import UpdateWorkoutCommand
from Backend.trainings.domain.exceptions.workout_exceptions import (
    Forbidden,
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

        if workout.user_id != command.user_id:
            raise Forbidden()

        workout.update(
            name=command.name, description=command.description, public=command.public
        )

        return await self.workout_repo.update(workout)
