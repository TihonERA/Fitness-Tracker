from fastapi import APIRouter, Depends, status, Path, HTTPException, Body
from typing import Annotated, List
from uuid import UUID
from pydantic import HttpUrl, ValidationError
from starlette.status import HTTP_200_OK
from ...schemas.workout import UpdateWorkout, WorkoutResponse, WorkoutScheme, WorkoutsFilter, TrainingDayScheme, DayExercisesScheme, UpdateWorkout, UpdateTrainingDays, UpdateDayExercise
from ...services.WorkoutService import WorkoutService
from ...utils.validators import DataNotModified, NotFound
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
) -> list[WorkoutResponse]:
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

@router.post(
    "/workouts/{workout_id}/training_day",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK
)
async def create_training_day_in_workout(
    workout_id: Annotated[int, Path()],
    training_day_scheme: Annotated[TrainingDayScheme, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
) -> WorkoutResponse:
    try:
        return await workout_service.create_training_day(
            workout_id=workout_id,
            training_day_scheme=training_day_scheme
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))

@router.post(
    "/workouts/{workout_id}/{training_day_id}/day_exercise",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK
)
async def create_day_exercise_in_training_day(
    workout_id: Annotated[int, Path()],
    training_day_id: Annotated[int, Path()],
    day_exercise_scheme: Annotated[DayExercisesScheme, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
) -> WorkoutResponse:
    try:
        return await workout_service.create_day_exercise(
            workout_id=workout_id,
            training_day_id=training_day_id,
            day_exercise_scheme=day_exercise_scheme
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))

@router.patch(
    "/workouts/{workout_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_workout(
    workout_id: Annotated[int, Path()],
    workout_update_data: Annotated[UpdateWorkout, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
) -> WorkoutResponse:
    try:
        return await workout_service.update_workout(
            workout_id=workout_id,
            workout_update_data=workout_update_data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.patch(
    "/woprkouts/{workout_id}/training_day/{training_day_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_training_days_in_workout(
    workout_id: Annotated[int, Path()],
    training_day_id: Annotated[int, Path()],
    training_day_update_data: Annotated[UpdateTrainingDays, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
) -> WorkoutResponse:
    try:
        return await workout_service.update_training_days(
            workout_id=workout_id,
            training_day_id=training_day_id,
            training_day_update_data=training_day_update_data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.patch(
    "/workouts/{workout_id}/day_exercise",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_day_exercise(
    workout_id: Annotated[int, Path()],
    day_exercises_update_data: Annotated[List[UpdateDayExercise], Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
) -> WorkoutResponse:
    try:
        return await workout_service.update_day_exercise(
           workout_id=workout_id,
           data=day_exercises_update_data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
