from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.training_day_exceptions import (
    TrainingDayNotCreatedError,
    TrainingDayNotFound,
)
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.infrastructure.mappers.training_day_mapper import (
    TrainingDayMapper,
)
from Backend.trainings.infrastructure.models import workout
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel


class TrainingDayRepository:
    def __init__(self, session: AsyncSession, mapper: TrainingDayMapper) -> None:
        self.session = session
        self.mapper = mapper

    async def _get_model(self, id: int) -> TrainingDayModel:
        training_day_model = await self.session.get(
            TrainingDayModel, id, options=[selectinload(TrainingDayModel.day_exercises)]
        )

        if training_day_model is None:
            raise TrainingDayNotFound(id)

        return training_day_model

    async def get(self, id: int) -> TrainingDay:
        training_day_model = await self._get_model(id)

        return self.mapper.to_domain(training_day_model)

    async def create(self, training_day: TrainingDay) -> TrainingDay:
        try:
            training_day_model = self.mapper.to_orm(training_day)

            self.session.add(training_day_model)
            await self.session.flush()

            return self.mapper.to_domain(training_day_model)
        except IntegrityError as e:
            raise NotImplementedError("Integrity")

    @staticmethod
    def _save_exercise(
        day_exercises_model: DayExerciseModel, day_exercises: DayExercise
    ) -> DayExerciseModel:
        day_exercises_model.exercise_order = day_exercises.exercise_order.value

        return day_exercises_model

    def _save_exercises(
        self,
        day_exercises_model: list[DayExerciseModel],
        day_exercises: list[DayExercise],
    ) -> list[DayExerciseModel]:
        existing_exercises = {e.exercise_id: e for e in day_exercises_model}

        updated_exercises = [
            (
                self._save_exercise(existing_exercises[e.exercise_id], e)
                if e.exercise_id in existing_exercises
                else self.mapper.to_orm_day_exercise(e)
            )
            for e in day_exercises
        ]

        return updated_exercises

    async def save(self, training_day: TrainingDay) -> TrainingDay:
        try:
            if training_day.id is None:
                raise TrainingDayNotCreatedError()
            training_day_model = await self._get_model(training_day.id)

            training_day_model.name = training_day.name.value
            training_day_model.day_order = training_day.day_order.value
            training_day_model.day_exercises = self._save_exercises(
                training_day_model.day_exercises, training_day.day_exercises
            )

            await self.session.flush()

            return self.mapper.to_domain(training_day_model)
        except IntegrityError as e:
            raise NotImplementedError()
