from fastapi import APIRouter, Depends
from ...schemas.workout import WorkoutResponse, WorkoutScheme
from ...services.WorkoutService import WorkoutService
from ..deps import get_workout_service

router = APIRouter(tags=["Workout Tables Endpoints"])

@router.post("/workout/workout_schedule", response_model=WorkoutResponse)
async def create_workout_with_schedule(
        data: WorkoutScheme,
        workout_service: WorkoutService = Depends(get_workout_service)
    ) -> WorkoutResponse:
    return await workout_service.create_workout_with_schedule(data)