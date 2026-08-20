from typing import Any
import uuid

import pytest
from redis.asyncio import Redis, RedisCluster

from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.workout import ListWorkoutResponse, WorkoutCreate, WorkoutGetAllFilter, WorkoutGetAllFilterDTO, WorkoutRelationsResponse, WorkoutUpdate
from Backend.services.WorkoutService import WorkoutService
from Backend.utils.exceptions import Forbidden, NotFound
from Backend.utils.uow import UnitOfWork

from sqlalchemy.ext.asyncio import AsyncSession

import random

from faker import Faker

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutService:

    @pytest.fixture
    def service(self, uow: UnitOfWork):
        return WorkoutService(uow=uow)

    @pytest.mark.parametrize("data", 
        [
            WorkoutCreate(name="Cardio", description="Cool Training", public=True),
            WorkoutCreate(name="Full Body", description=None, public=False)
        ],
        ids=["full_data", "missing_description_false_public"]
    )
    async def test_create_workout_success(
        self, 
        data,
        service: WorkoutService,
        user: User
    ):
        workout = await service.create_workout(user_id=user.id, data=data)

        assert workout.user_id == user.id
        assert workout.name == data.name
        assert workout.description == data.description
        assert workout.public == data.public

    async def test_create_workout_foreign_key_violation(
        self,
        service: WorkoutService
    ):
        data = WorkoutCreate(name="Cardio", description="Cool Training", public=True)

        with pytest.raises(NotFound):
            await service.create_workout(user_id=uuid.uuid4(), data=data)

    async def test_get_loaded_workouts(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        fetched_workout = await service.get_loaded_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        assert isinstance(fetched_workout, Workout)
        assert len(fetched_workout.training_days) > 0
        assert len(fetched_workout.training_days[0].day_exercises) > 0

    async def test_update_workout_success(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        data = WorkoutUpdate(
            name="newname",
            description="newdescription",
            public=random.choice([True, False])
        )

        updated_workout = await service.update_workout(
            user_id=workout.user_id,
            workout_id=workout.id,
            data=data
        )

        assert updated_workout.name == data.name
        assert updated_workout.description == data.description
        assert updated_workout.public == data.public

    async def test_delete_workout_success(
        self,
        service: WorkoutService,
        workout: Workout
    ):
        fetched_workout = await service.get_loaded_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        assert fetched_workout is not None

        await service.delete_workout(
            user_id=workout.user_id,
            workout_id=workout.id
        )

        with pytest.raises(NotFound):
            await service.get_loaded_workout(
                user_id=workout.user_id,
                workout_id=workout.id
            )
