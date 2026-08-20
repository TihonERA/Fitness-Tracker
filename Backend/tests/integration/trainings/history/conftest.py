from dataclasses import dataclass
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models.exercise_history import ExerciseHistory
from Backend.models.training_day_history import TrainingDayHistory
from Backend.models.workout import Workout

@dataclass
class TrDayData:
    user_id: UUID 
    workout_id: int
    history: TrainingDayHistory 

@dataclass
class TrDayDatas:
    user_id: UUID
    workout_id: int
    histories: list[TrainingDayHistory] 

@pytest.fixture
async def tr_day_history(workout: Workout, db_session: AsyncSession):
    day = workout.training_days[0]

    exercise_history = ExerciseHistory(
        user_id=workout.user_id,
        exercise_id=workout.training_days[0].day_exercises[0].exercise_id,
    )
    history = TrainingDayHistory(
        day_id=day.id,
        day_name=day.name,
        exercises_history=[exercise_history]
    )

    db_session.add(history)
    await db_session.commit()

    data = TrDayData(
        user_id=workout.user_id,
        workout_id=workout.id,
        history=history
    )

    return data

@pytest.fixture
async def tr_day_histories(workout: Workout, db_session):
    days = [
        workout.training_days[0],
        workout.training_days[1],
        workout.training_days[2]
    ]
    histories = []
    for day in days:
        history = TrainingDayHistory(
            day_id=day.id,
            day_name=day.name
        )
        histories.append(history)
        db_session.add(history)

    await db_session.commit()

    data = TrDayDatas(
        user_id=workout.user_id,
        workout_id=workout.id,
        histories=histories
    )
    return data

