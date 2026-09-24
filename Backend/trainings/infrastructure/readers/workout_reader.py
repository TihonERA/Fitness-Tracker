from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.trainings.application.dto.training_day import (
    TrainingDayReadDTO,
)
from Backend.trainings.application.dto.workout import WorkoutDetailDTO
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel


class WorkoutReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_loaded(self, id: int) -> WorkoutDetailDTO | None:
        workout = await self.session.get(
            WorkoutModel, id, options=[selectinload(WorkoutModel.training_days)]
        )

        if workout is None:
            return None

        return self._to_dto(workout)

    def _to_dto_tr_day(self, training_day: TrainingDayModel) -> TrainingDayReadDTO:
        return TrainingDayReadDTO(
            id=training_day.id,
            workout_id=training_day.workout_id,
            name=training_day.name,
            day_order=training_day.day_order,
        )

    def _to_dto(self, workout: WorkoutModel) -> WorkoutDetailDTO:
        return WorkoutDetailDTO(
            id=workout.id,
            user_id=workout.user_id,
            name=workout.name,
            description=workout.description,
            public=workout.public,
            training_days=[self._to_dto_tr_day(t) for t in workout.training_days],
        )
