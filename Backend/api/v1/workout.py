from fastapi import APIRouter, Depends, status, Path, HTTPException, Query, Body
from typing import Annotated
from uuid import UUID
from ...schemas.workout import WorkoutResponse, WorkoutScheme, WorkoutsFilter
from ...services.WorkoutService import WorkoutService
from ...utils.validators import NotFound
from ..deps import get_workout_service, get_workouts_filter

router = APIRouter(
    tags=["Workout Tables Endpoints"]
)

@router.get(
    "/workouts",
    response_model=list[WorkoutResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_workouts(
    user_id: UUID,
    filter: Annotated[WorkoutsFilter, Depends(get_workouts_filter)],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    return await workout_service.get_all_workouts(
        filter=filter,
        user_id=user_id
    )

@router.get(
    "/workouts/{workout_id}",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK      
)
async def get_workout(
    workout_id: Annotated[int, Path()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
    ) -> WorkoutResponse:
    try:
        return await workout_service.get_workout(workout_id)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post(
    "/workouts/workout_schedule", 
    response_model=WorkoutResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_workout_with_schedule(
        data: Annotated[WorkoutScheme, Body()],
        workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
    ) -> WorkoutResponse:
    return await workout_service.create_workout_with_schedule(data)