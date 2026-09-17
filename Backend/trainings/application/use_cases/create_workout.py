from Backend.trainings.application.dto.workout import CreateWorkoutCommand
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository
from Backend.trainings.domain.workout_model import Workout


class CreateWorkoutUseCase:
    def __init__(self, workout_repo: IWorkoutRepository) -> None:
        self.workout_repo = workout_repo

    async def __call__(self, command: CreateWorkoutCommand) -> Workout:
        workout = Workout.create(
            user_id=command.user_id,
            name=command.name,
            description=command.description,
            public=command.public,
        )

        return await self.workout_repo.create(workout)
