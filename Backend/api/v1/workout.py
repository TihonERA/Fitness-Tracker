from fastapi import APIRouter, Depends, Response, status, HTTPException, Body
from typing import Annotated
from uuid import UUID
from pydantic import ValidationError
from starlette.status import HTTP_200_OK
from Backend.tasks.muscle_rates import get_muscle_contribution_list, get_muscles_balance
from Backend.schemas.workout import ListWorkoutResponse, WorkoutCreate, WorkoutRelationsResponse, WorkoutResponse, WorkoutGetAllFilter, WorkoutUpdate
from Backend.api.deps import GetCurrentUserDepends, WorkoutProxyDepends, get_workouts_filter, IntPath

router = APIRouter(
    tags=["Workout Tables Endpoints"],
    prefix="/workouts"
)

@router.get(
    "/get_all",
    status_code=status.HTTP_200_OK
)
async def get_all_workouts(
    user_id: GetCurrentUserDepends,
    data: Annotated[WorkoutGetAllFilter, Depends(get_workouts_filter)],
    w_proxy: WorkoutProxyDepends 
) -> ListWorkoutResponse:
    return await w_proxy.get_all_workouts(
        user_id=user_id,
        data=data,
    )

@router.get(
    "/{workout_id}",
    response_model=WorkoutRelationsResponse,
    status_code=status.HTTP_200_OK      
)
async def get_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath, 
    w_proxy: WorkoutProxyDepends,
) -> WorkoutRelationsResponse:
    return await w_proxy.get_loaded_workout(
        user_id=user_id,
        workout_id=workout_id
    )

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED
)
async def create_workout(
    user_id: GetCurrentUserDepends,
    data: Annotated[WorkoutCreate, Body()],
    w_proxy: WorkoutProxyDepends
) -> WorkoutResponse:
    return await w_proxy.create_workout(
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
    w_proxy: WorkoutProxyDepends
) -> WorkoutResponse:
    return await w_proxy.update_workout(
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
    w_proxy: WorkoutProxyDepends
):
    return await w_proxy.delete_workout(
        user_id=user_id,
        workout_id=workout_id
    )
