from os import stat
import re

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import descriptor_props, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption
from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel
from typing import Sequence, Any, final
from uuid import UUID


@final
class WorkoutRepository(IWorkoutRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _make_day_exercise_model(self, exercise_model: DayExerciseModel) -> DayExercise:
        return DayExercise(
            day_id=exercise_model.day_id,
            exercise_id=exercise_model.exercise_id,
            day_order=exercise_model.day_order,
        )

    def _make_training_day_model(self, day_model: TrainingDayModel) -> TrainingDay:
        return TrainingDay(
            id=day_model.id,
            workout_id=day_model.workout_id,
            name=day_model.name,
            day_exercises=[
                self._make_day_exercise_model(e) for e in day_model.day_exercises
            ],
        )

    async def _get_template(
        self, id: int, options: list[ORMOption] | None = None
    ) -> Workout | None:
        stmt = select(WorkoutModel).where(WorkoutModel.id == id)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()

        if result is None:
            return None

        return Workout(
            id=result.id,
            user_id=result.user_id,
            name=result.name,
            description=result.description,
            public=result.public,
            training_days=(
                [self._make_training_day_model(d) for d in result.training_days]
                if options
                else []
            ),
        )

    async def get(self, id: int) -> Workout | None:
        return await self._get_template(id)

    async def get_loaded(self, id: int) -> Workout | None:
        return await self._get_template(
            id=id,
            options=[
                selectinload(WorkoutModel.training_days).selectinload(
                    TrainingDayModel.day_exercises
                )
            ],
        )

    async def create(self, workout: Workout) -> Workout:
        try:
            workout_model = WorkoutModel(
                user_id=workout.user_id,
                name=workout.name,
                description=workout.description,
                public=workout.public,
            )  # Не подразумевается каскадное создание записей

            self.session.add(workout_model)
            await self.session.flush()

            return WorkoutModel(
                id=workout_model.id,
                user_id=workout_model.user_id,
                name=workout_model.name,
                description=workout_model.description,
                public=workout_model.public,
                training_days=[],
            )
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    async def update(self, workout: Workout) -> Workout:
        try:
            workout_model = await self.session.get(WorkoutModel, workout.id)

            if workout_model is None:
                raise WorkoutNotFound()

            workout_model.name = workout.name
            workout_model.description = workout.description
            workout_model.public = workout.public

            await self.session.flush()

            return Workout(
                id=workout_model.id,
                user_id=workout_model.user_id,
                name=workout_model.name,
                description=workout_model.description,
                public=workout_model.public,
                training_days=workout.training_days,
            )  # Если есть загруженные связи, то просто передаем, этот метод отвечает за обновление Workout, а не обновление связей
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    async def delete(self, workout: Workout) -> None:
        try:
            await self.session.delete(workout)
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
