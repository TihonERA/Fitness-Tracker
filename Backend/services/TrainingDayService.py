from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.workout import Workout
from Backend.repositories.WorkoutRepository import WorkoutRepository
from Backend.schemas.workout import TrainingDayCreate, TrainingDayUpdate
from Backend.services.DayExerciseService import DayExerciseService
from Backend.utils.decorators import invalidate_cache
from ..utils.validators import NotFound
from ..repositories.TrainingDayRepository import TrainingDayRepository
from ..models.trainingday import TrainingDay

class TrainingDayService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.trdayrepo = TrainingDayRepository(session=session)
        self.dayexeservice = DayExerciseService(session=session)
        self.workoutrepo = WorkoutRepository(session=session)

    @invalidate_cache(column=Workout.workout_id)
    async def create_training_day(
        self,
        workout_id: int,
        data: TrainingDayCreate
    ):
        training_day = TrainingDay(
            workout_id=workout_id,
            name=data.name,
            day_order=data.day_order
        )

        training_day = await self.trdayrepo.create_instance(instance=training_day)

        for day_exer in data.day_exercises:
            await self.dayexeservice.create_day_exercise(
                day_id=training_day.day_id,
                data=day_exer
            )

            
        return training_day

    @invalidate_cache(column=Workout.workout_id)
    async def update_training_day(
        self,
        day_id: int,
        data: TrainingDayUpdate
    ):
        result = await self.trdayrepo.update_training_day(
            day_id=day_id,
            data=data.model_dump(exclude_unset=True)
        )
        if result is None:
            raise NotFound()

        return result

    @invalidate_cache(column=Workout.workout_id)
    async def delete_training_day(
        self,
        workout_id: int,
        day_id: int
    ):
        workout = await self.workoutrepo.get_workout(workout_id=workout_id)
        if workout is None:
            raise NotFound()

        tr_day = next((d for d in workout.training_days if d.day_id == day_id), None)
        if tr_day is None:
            raise NotFound()

        await self.trdayrepo.delete_training_day(
            day_id=day_id
        )

        return tr_day
