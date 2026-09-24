from typing import Protocol
from uuid import UUID

from Backend.trainings.application.dto.workout import WorkoutDetailDTO
from Backend.trainings.domain.exceptions.workout_exceptions import (
    WorkoutAccessDenied,
    WorkoutNotFound,
)


class WorkoutReader(Protocol):
    async def get_loaded(self, id: int) -> WorkoutDetailDTO | None: ...


class GetLoadedWorkoutUseCase:
    def __init__(self, workout_reader: WorkoutReader) -> None:
        self.workout_reader = workout_reader

    async def __call__(self, user_id: UUID, workout_id: int) -> WorkoutDetailDTO:
        workout = await self.workout_reader.get_loaded(workout_id)

        if workout is None:
            raise WorkoutNotFound(workout_id)

        if workout.public:
            return workout

        if workout.user_id != user_id:
            raise WorkoutAccessDenied()

        return workout
