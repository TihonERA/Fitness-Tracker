from typing import Annotated

from fastapi import APIRouter, Body, status

from Backend.api.deps import DayExerciseServiceDepends, GetCurrentUserDepends, IntPath
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseResponse, DayExerciseUpdate

router = APIRouter(
    tags=["DayExercise Table Endpoints"],
    prefix="/day_exercises"
)

@router.get(
    "/{workout_id}/{day_id}/{exercise_id}",
    response_model=DayExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def get_day_exercise(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    exercise_id: IntPath,
    dayexerservice: DayExerciseServiceDepends
):
    return await dayexerservice.get_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        exercise_id=exercise_id
    )

@router.post(
    "/{workout_id}/{day_id}",
    response_model=DayExerciseResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_day_exercise(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    data: Annotated[DayExerciseCreate, Body()],
    dayexerservice: DayExerciseServiceDepends
):
    return await dayexerservice.create_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        data=data
    )

@router.patch(
    "/{workout_id}/{day_id}/{exercise_id}",
    response_model=DayExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def update_day_exercise(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    exercise_id: IntPath,
    data: Annotated[DayExerciseUpdate, Body()],
    dayexerservice: DayExerciseServiceDepends
):
    return await dayexerservice.update_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        exercise_id=exercise_id,
        data=data
    )

@router.delete(
    "/{workout_id}/{day_id}/{exercise_id}",
    response_model=DayExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def delete_day_exercise(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    exercise_id: IntPath,
    dayexerservice: DayExerciseServiceDepends
):
    return await dayexerservice.delete_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        exercise_id=exercise_id
    )
