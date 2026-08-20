import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import random

from faker import Faker

from Backend.models.user import User
from Backend.models.workout import Workout
from Backend.models.trainingday import TrainingDay
from Backend.models.dayexercise import DayExercise

@pytest.fixture
async def workout(db_session: AsyncSession, user: User):
    day_1 = TrainingDay(name="Тренировка спины и бицепса", day_order=1)
    day_2 = TrainingDay(name="Тренировка груди, плеч и трицепса", day_order=2)
    day_3 = TrainingDay(name="Тренировка ног и пресса", day_order=3)

    ex_1_1 = DayExercise(exercise_id=9, exercise_order=1, training_day=day_1)
    ex_1_2 = DayExercise(exercise_id=10, exercise_order=2, training_day=day_1)
    ex_1_3 = DayExercise(exercise_id=11, exercise_order=3, training_day=day_1)
    ex_1_4 = DayExercise(exercise_id=18, exercise_order=4, training_day=day_1)
    ex_1_5 = DayExercise(exercise_id=29, exercise_order=5, training_day=day_1)
    ex_1_6 = DayExercise(exercise_id=43, exercise_order=6, training_day=day_1)

    ex_2_1 = DayExercise(exercise_id=3, exercise_order=1, training_day=day_2)
    ex_2_2 = DayExercise(exercise_id=5, exercise_order=2, training_day=day_2)
    ex_2_3 = DayExercise(exercise_id=21, exercise_order=3, training_day=day_2)
    ex_2_4 = DayExercise(exercise_id=22, exercise_order=4, training_day=day_2)
    ex_2_5 = DayExercise(exercise_id=37, exercise_order=5, training_day=day_2)
    ex_2_6 = DayExercise(exercise_id=45, exercise_order=6, training_day=day_2)

    ex_3_1 = DayExercise(exercise_id=47, exercise_order=1, training_day=day_3)
    ex_3_2 = DayExercise(exercise_id=17, exercise_order=2, training_day=day_3)
    ex_3_3 = DayExercise(exercise_id=52, exercise_order=3, training_day=day_3)
    ex_3_4 = DayExercise(exercise_id=59, exercise_order=4, training_day=day_3)
    ex_3_5 = DayExercise(exercise_id=42, exercise_order=5, training_day=day_3)
    ex_3_6 = DayExercise(exercise_id=40, exercise_order=6, training_day=day_3)

    day_1.day_exercises = [ex_1_1, ex_1_2, ex_1_3, ex_1_4, ex_1_5, ex_1_6]
    day_2.day_exercises = [ex_2_1, ex_2_2, ex_2_3, ex_2_4, ex_2_5, ex_2_6]
    day_3.day_exercises = [ex_3_1, ex_3_2, ex_3_3, ex_3_4, ex_3_5, ex_3_6]

    workout = Workout(
        user_id=user.id,
        name="testworkout",
        description="testdescription",
        training_days=[
            day_1, day_2,day_3        
        ]
    ) 

    db_session.add(workout)
    await db_session.flush()

    stmt = (
        select(Workout)
        .where(Workout.id == workout.id)
        .options(
            selectinload(Workout.training_days)
            .selectinload(TrainingDay.day_exercises)
        )
    )
    workout = await db_session.execute(stmt)
    await db_session.commit()
    return workout.scalar()
