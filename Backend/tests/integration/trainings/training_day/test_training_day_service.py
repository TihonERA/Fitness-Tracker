import pytest
from redis.asyncio.cluster import _unregister_slots_cache_listener

from Backend.models.workout import Workout
from Backend.schemas.training_day import TrainingDayCreateDTO, TrainingDayUpdate
from Backend.services.TrainingDayService import TrainingDayService
from Backend.utils.exceptions import NotFound
from Backend.utils.uow import UnitOfWork

from faker import Faker

@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        return TrainingDayService(uow=uow)

    async def test_create_training_day(
        self,
        service: TrainingDayService,
        workout: Workout,
        faker: Faker
    ):
        data = TrainingDayCreateDTO(
            name=faker.name(),
            day_order=len(workout.training_days)+1,
            workout_id=workout.id
        )

        created_training_day = await service.create_training_day(
            user_id=workout.user_id,
            data=data
        )

        assert created_training_day.name == data.name
        assert created_training_day.day_order == data.day_order
        assert created_training_day.workout_id == data.workout_id

    async def test_update_training_day(
        self,
        service: TrainingDayService,
        workout: Workout
    ):
        data = TrainingDayUpdate(
            name="newname"
        )

        updated_training_day = await service.update_training_day(
            user_id=workout.user_id,
            workout_id=workout.id,
            day_id=workout.training_days[0].id,
            data=data
        )

        assert updated_training_day.name == data.name

    async def test_delete_training_day(
        self,
        service: TrainingDayService,
        workout: Workout
    ):
        day_id = workout.training_days[0].id

        await service.delete_training_day(
            user_id=workout.user_id,
            workout_id=workout.id,
            day_id=day_id
        )

        async with service.uow as uow:
            assert await uow.trainingday.get_instance_by_id(id=day_id) is None

