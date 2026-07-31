from fastapi import APIRouter, Depends, Response, status, HTTPException, Body
from typing import Annotated
from uuid import UUID
from pydantic import ValidationError
from starlette.status import HTTP_200_OK
from Backend.tasks.muscle_rates import get_muscle_contribution_list, get_muscles_balance
from ...schemas.workout import WorkoutCreate, WorkoutRelationsResponse, WorkoutResponse, WorkoutGetAllFilter, WorkoutUpdate
from ...utils.validators import DataNotModified, NotFound
from ..deps import DayExerciseServiceDepends, GetCurrentUserDepends, TrainingDayServiceDepends, WorkoutServiceDepends, get_workouts_filter, IntPath

router = APIRouter(
    tags=["Workout Tables Endpoints"],
    prefix="/workouts"
)

@router.get(
    "/get_all",
    response_model=list[WorkoutResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_workouts(
    filter: Annotated[WorkoutGetAllFilter, Depends(get_workouts_filter)],
    workout_service: WorkoutServiceDepends
):
    return await workout_service.get_all_workouts(
        filter=filter,
    )

@router.get(
    "/{workout_id}",
    response_model=WorkoutRelationsResponse,
    status_code=status.HTTP_200_OK      
)
async def get_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath, 
    workout_service: WorkoutServiceDepends,
):
    return await workout_service.get_workout(
        workout_id=workout_id,
        user_id=user_id
    )

@router.post(
    "/{workout_id}/muscles_distribution_list",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=str
)
def calculate_muscles_distribution_list(
    workout_id: IntPath,
): 
    task = get_muscle_contribution_list.delay(workout_id)
    return task.id

@router.post(
    "/{workout_id}/muscles_balance_list",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=str
)
def calculate_muscles_balance(
    workout_id: IntPath
) -> str:
    task = get_muscles_balance.delay(workout_id)
    return task.id

@router.post(
    "/", 
    response_model=WorkoutResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_workout(
    user_id: GetCurrentUserDepends,
    data: Annotated[WorkoutCreate, Body()],
    workout_service: WorkoutServiceDepends
):
    return await workout_service.create_workout(
        user_id=user_id,
        data=data
    )

@router.patch(
    "/{workout_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    data: Annotated[WorkoutUpdate, Body()],
    workout_service: WorkoutServiceDepends
):
    return await workout_service.update_workout(
        user_id=user_id,
        workout_id=workout_id,
        data=data
    )

@router.delete(
    "/{workout_id}",
    status_code=HTTP_200_OK,
    response_model=WorkoutResponse
)
async def delete_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    workout_service: WorkoutServiceDepends
):
    return await workout_service.delete_workout(
        user_id=user_id,
        workout_id=workout_id
    )
