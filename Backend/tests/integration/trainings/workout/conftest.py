import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.user import User
from Backend.models.workout import Workout

import random

from faker import Faker

@pytest.fixture
async def random_workouts(user: User, db_session: AsyncSession, faker: Faker):
    workouts = []
    for _ in range(1, 11):
        workout = Workout(
            user_id=user.id, 
            name=faker.catch_phrase(),
            description=faker.paragraph(nb_sentences=3),
            public=random.choice([True, False])
        )
        db_session.add(workout)
        await db_session.flush()
            
        workouts.append(workout)
        
    return workouts

