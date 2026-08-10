from typing import Any
import uuid

import pytest
from redis.asyncio import Redis

from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.workout import ListWorkoutResponse, WorkoutCreate, WorkoutGetAllFilter
from Backend.services.WorkoutService import WorkoutService
from Backend.utils.exceptions import NotFound
from Backend.utils.uow import UnitOfWork

from sqlalchemy.ext.asyncio import AsyncSession

from faker import Faker

@pytest.mark.asyncio(loop_scope="session")
class TestWorkoutService:

    @pytest.fixture
    def service(self, uow: UnitOfWork, redis: Redis):
        return WorkoutService(uow=uow, redis=redis)

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

        
    async def test_get_all_workouts_cache(
        self,
        service: WorkoutService,
        db_session: AsyncSession,
        workout: Workout
    ):
        redis = service.redis 

        filter = WorkoutGetAllFilter(
            skip=0,
            limit=50,
            user_id=workout.user_id
        )
        db_result = await service.get_all_workouts(user_id=workout.user_id, filter=filter)
        
        caches = [key async for key in redis.scan_iter(match="workouts:all:*")]

        assert len(caches) > 0

        await db_session.delete(workout)

        cache_result = await service.get_all_workouts(user_id=workout.user_id, filter=filter)

        assert isinstance(cache_result, (str, bytes))

        expected_data = ListWorkoutResponse.model_validate(db_result)
        actual_data = ListWorkoutResponse.model_validate_json(cache_result)

        assert expected_data == actual_data

        
    async def test_get_all_workouts_access_rights(
        self,
        service: WorkoutService,
        db_session: AsyncSession,
        random_workouts: list[Workout]
    ):
        for workout in random_workouts:
            db_session.add(workout)

        await db_session.flush()

        filter = WorkoutGetAllFilter(
            skip=0,
            limit=50,
            user_id=random_workouts[0].user_id,
            public=False
        )

        fetched_workouts = await service.get_all_workouts(
            user_id=uuid.uuid4(),
            filter=filter
        )
        
        assert isinstance(fetched_workouts, list)

        assert all([workout.public == True for workout in fetched_workouts])
