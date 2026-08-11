from os import name
from typing import Any
from uuid import UUID, uuid4
import uuid

from faker import Faker
import pytest
from redis.asyncio import Redis

import random

from Backend.models.workout import Workout
from Backend.schemas.workout import WorkoutCreate, WorkoutCreateDTO, WorkoutGetAllFilter
from Backend.services.WorkoutService import WorkoutService
from Backend.utils.exceptions import Forbidden, NotFound
from Backend.utils.uow import UnitOfWork

from Backend.tests.unit.conftest import user_id

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutService:

    @pytest.fixture
    def service(self, uow: UnitOfWork, redis: Redis):
        return WorkoutService(uow=uow, redis=redis)

    async def test_create_workout_success(
        self, 
        service: WorkoutService, 
        user_id: UUID,
        faker: Faker
    ):
        mock_uow: Any = service.uow
        mock_uow.workout.create_instance.return_value = "fake_object"

        data = WorkoutCreate(
            name=faker.word(),
            description=faker.word(),
            public=True
        )
    
        result = await service.create_workout(user_id=user_id, data=data)

        assert result == "fake_object"

        mock_uow.workout.create_instance.assert_called_once()

        send_dto = mock_uow.workout.create_instance.call_args.kwargs["data"]

        assert isinstance(send_dto, WorkoutCreateDTO)
        assert send_dto.user_id == user_id
        assert send_dto.name == data.name
        assert send_dto.description == data.description
        assert send_dto.public == data.public
        
    @pytest.fixture
    def workout(self, user_id, faker):
        workout = Workout(
            id=1, 
            user_id=user_id, 
            name=faker.word(), 
            description=faker.word(), 
            public=False
        )
        return workout

    async def test_get_workout(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        mock_uow: Any = service.uow
        mock_uow.workout.get_workout.return_value = workout

        created_workout = await service.get_workout(workout_id=workout.id, user_id=workout.user_id)

        assert created_workout == workout

    async def test_get_workout_forbidden(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        mock_uow: Any = service.uow
        mock_uow.workout.get_workout.return_value = workout

        with pytest.raises(Forbidden):
            await service.get_workout(workout_id=workout.id, user_id=uuid4())

    async def test_get_workout_not_found(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        mock_uow: Any = service.uow
        mock_uow.workout.get_workout.return_value = None

        with pytest.raises(NotFound):
            await service.get_workout(workout_id=-1, user_id=workout.user_id)
    
    async def test_get_all_workouts_dto(
        self,
        service: WorkoutService,
        mocker,
        random_workouts: list[Workout]
    ):
        mock_uow: Any = service.uow
        mock_uow.workout.get_all_workouts.return_value = random_workouts
        service.redis = mocker.AsyncMock()
        service.redis.get.return_value = None

        filter = WorkoutGetAllFilter(
            skip=0,
            limit=50,
            user_id=random_workouts[0].user_id,
            public=False
        )

        fetched_workouts = await service.get_all_workouts(user_id=uuid4(), filter=filter)

        mock_uow.workout.get_all_workouts.assert_called_once()

        send_dto = mock_uow.workout.get_all_workouts.call_args.kwargs["public"]

        assert send_dto
