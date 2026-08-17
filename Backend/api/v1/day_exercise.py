from typing import Annotated

from fastapi import APIRouter, Body, status

from Backend.api.deps import DayExerciseProxyDepends, GetCurrentUserDepends, IntPath
from Backend.schemas.day_exercise import DayExerciseCreate, DayExerciseResponse

router = APIRouter(
    tags=["DayExercise Table Endpoints"],
    prefix="/day_exercises"
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
    de_proxy: DayExerciseProxyDepends
):
    return await de_proxy.create_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
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
    de_proxy: DayExerciseProxyDepends
):
    return await de_proxy.delete_day_exercise(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        exercise_id=exercise_id
    )
