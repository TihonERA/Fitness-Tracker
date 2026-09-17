from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption
from Backend.trainings.domain.day_exercise_model import DayExercise
from Backend.trainings.domain.exceptions.workout_exceptions import WorkoutNotFound
from Backend.trainings.domain.ports.workout_repository import IWorkoutRepository
from Backend.trainings.domain.training_day_model import TrainingDay
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.mappers.workout_mapper import WorkoutMapper
from Backend.trainings.infrastructure.models.dayexercise import DayExerciseModel
from Backend.trainings.infrastructure.models.trainingday import TrainingDayModel
from Backend.trainings.infrastructure.models.workout import WorkoutModel
from typing import Sequence, Any, final
from uuid import UUID


@final
class WorkoutRepository(IWorkoutRepository):

    def __init__(self, session: AsyncSession, mapper: WorkoutMapper):
        self.session = session
        self.mapper = mapper

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

        return (
            self.mapper.to_domain_with_training_days(result)
            if options
            else self.mapper.to_domain(result)
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
            workout_model = self.mapper.to_orm(workout)
            self.session.add(workout_model)
            await self.session.flush()

            return self.mapper.to_domain(workout_model)
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

            return self.mapper.to_domain_with_inherited_training_days(
                workout_model=workout_model,
                inherited_training_days=workout.training_days,
            )
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
