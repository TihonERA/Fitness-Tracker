from typing import Any
import uuid

import pytest
from redis.asyncio import Redis

from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.schemas.workout import WorkoutCreate, WorkoutGetAllFilter
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
        result1 = await service.get_all_workouts(filter=filter)
        
        caches = [key async for key in redis.scan_iter(match="workouts:all:*")]

        assert len(caches) > 0

        await db_session.delete(workout)

        result2 = await service.get_all_workouts(filter=filter)

        assert result2 != []
        assert result1 == result2
