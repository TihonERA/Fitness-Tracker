from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption
from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.mappers.workout_mapper import WorkoutMapper
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel
from typing import Sequence, Any, final
from uuid import UUID


class WorkoutRepository:

    def __init__(self, session: AsyncSession, mapper: WorkoutMapper):
        self.session = session
        self.mapper = mapper

    async def get(self, id: int) -> Workout | None:
        workout_model = await self.session.get(WorkoutModel, id)

        if workout_model is None:
            return None

        return self.mapper.to_domain(workout_model)

    async def create(self, workout: Workout) -> Workout:
        try:
            workout_model = self.mapper.to_orm(workout)
            self.session.add(workout_model)
            await self.session.flush()

            return self.mapper.to_domain(workout_model)
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    async def save(self, workout: Workout) -> Workout | None:
        try:
            workout_model = await self.session.get(WorkoutModel, workout.id)

            if workout_model is None:
                return None

            workout_model.name = workout.name.value
            workout_model.description = workout.description
            workout_model.public = workout.public

            await self.session.flush()

            return self.mapper.to_domain(workout_model)
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    async def delete(self, id: int) -> None:
        try:
            stmt = delete(WorkoutModel).where(WorkoutModel.id == id)
            await self.session.execute(stmt)
            await self.session.flush()
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    # Справочный матерьял для рефакторинга метода get_all
    # async def get_all(self, data: WorkoutGetAllFilterDTO) -> Sequence[Workout]:
    #     stmt = select(Workout)
    #     if data.target_user_id:
    #         stmt = stmt.where(
    #             Workout.user_id == data.target_user_id,
    #         )
    #     if data.public:
    #         stmt = stmt.where(Workout.public == data.public)
    #     stmt = stmt.offset(data.skip).limit(data.limit)
    #
    #     result = await self.execute(stmt)
    #     return result.scalars().all()
