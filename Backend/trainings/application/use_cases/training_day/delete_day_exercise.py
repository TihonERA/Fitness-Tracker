from uuid import UUID

from Backend.trainings.application.ports.training_day import (
    TrainingDayAccessServicePort,
    TrainingDayRepositoryPort,
)
from Backend.trainings.domain.training_day_model import TrainingDay


class DeleteDayExerciseUseCase:
    def __init__(
        self,
        access_service: TrainingDayAccessServicePort,
        tr_day_repo: TrainingDayRepositoryPort,
    ) -> None:
        self.access_service = access_service
        self.tr_day_repo = tr_day_repo

    async def __call__(
        self, user_id: UUID, workout_id: int, day_id: int, exercise_id: int
    ) -> TrainingDay:
        training_day = await self.access_service.get_authorized_day(
            user_id, workout_id, day_id
        )

        training_day.delete_exercise(exercise_id)

        return await self.tr_day_repo.save(training_day)
