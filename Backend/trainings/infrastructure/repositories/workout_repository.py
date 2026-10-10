from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.trainings.domain.workout_model import Workout
from Backend.trainings.infrastructure.mappers.workout_mapper import WorkoutMapper
from Backend.trainings.infrastructure.models.workout import WorkoutModel
from uuid import UUID


class WorkoutRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_model(self, id: int) -> WorkoutModel | None:
        return await self.session.get(WorkoutModel, id, with_for_update=True)

    async def get(self, id: int) -> Workout | None:
        workout_model = await self._get_model(id)

        if workout_model is None:
            return None

        return WorkoutMapper.to_domain(workout_model)

    async def create(self, workout: Workout) -> Workout:
        try:
            workout_model = WorkoutMapper.to_orm(workout)
            self.session.add(workout_model)
            await self.session.flush()

            return WorkoutMapper.to_domain(workout_model)
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

            return WorkoutMapper.to_domain(workout_model)
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")

    async def delete(self, id: int) -> None:
        try:
            stmt = delete(WorkoutModel).where(WorkoutModel.id == id)
            await self.session.execute(stmt)
            await self.session.flush()
        except IntegrityError as e:
            raise NotImplementedError("Не реализован обработчик ошибки integrity")
