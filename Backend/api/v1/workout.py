from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated
from ...schemas.workout import WorkoutResponse, WorkoutScheme
from ...services.WorkoutService import WorkoutService
from ...utils.validators import NotFound
from ..deps import get_workout_service

router = APIRouter(
    tags=["Workout Tables Endpoints"]
)

@router.get(
    "/workout/{workout_id}",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK      
)
async def get_workout(
    workout_id: Annotated[int, Path()],
    workout_service: WorkoutService = Depends(get_workout_service)
    ) -> WorkoutResponse:
    try:
        return await workout_service.get_workout(workout_id)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post(
    "/workout/workout_schedule", 
    response_model=WorkoutResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_workout_with_schedule(
        data: WorkoutScheme,
        workout_service: WorkoutService = Depends(get_workout_service)
    ) -> WorkoutResponse:
    return await workout_service.create_workout_with_schedule(data)