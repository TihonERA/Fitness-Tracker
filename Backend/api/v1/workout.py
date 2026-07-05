from fastapi import APIRouter, Depends, Response, status, Path, HTTPException, Body
from typing import Annotated
from uuid import UUID
from pydantic import ValidationError
from starlette.status import HTTP_200_OK
from ...schemas.workout import DayExerciseCreate, DayExerciseUpdate, TrainingDayCreate, TrainingDayUpdate, WorkoutCreate, WorkoutMuscleDistribution, WorkoutResponse, WorkoutGetAllFilter, WorkoutUpdate
from ...services.WorkoutService import WorkoutService
from ...utils.validators import DataNotModified, NotFound
from ..deps import WorkoutServiceDepends, get_workout_service, get_workouts_filter, IntPath

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
    filter: Annotated[WorkoutGetAllFilter, Depends(get_workouts_filter)],
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
):
    try:
        return await workout_service.get_workout(workout_id)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get(
    "/workouts/{workout_id}/trained_muscles",
    response_model=list[WorkoutMuscleDistribution],
    status_code=status.HTTP_200_OK
)
async def get_muscles_distribution_list(
    workout_id: IntPath,
    workout_service: WorkoutServiceDepends
): 
    try:
        return await workout_service.get_muscles_distribution_list(
            workout_id=workout_id
        )
    except NotFound as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )

@router.post(
    "/workouts/workout_schedule", 
    response_model=WorkoutResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_workout_with_schedule(
    data: Annotated[WorkoutCreate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    return await workout_service.create_workout_with_schedule(data)

@router.post(
    "/workouts/{workout_id}/training_day",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK
)
async def create_training_day_in_workout(
    workout_id: Annotated[int, Path()],
    data: Annotated[TrainingDayCreate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        return await workout_service.create_training_day(
            workout_id=workout_id,
            data=data 
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
    data: Annotated[DayExerciseCreate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        return await workout_service.create_day_exercise(
            workout_id=workout_id,
            training_day_id=training_day_id,
            data=data
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
    data: Annotated[WorkoutUpdate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        return await workout_service.update_workout(
            workout_id=workout_id,
            data=data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.patch(
    "/workouts/{workout_id}/training_day/{training_day_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_training_days_in_workout(
    workout_id: Annotated[int, Path()],
    training_day_id: Annotated[int, Path()],
    data: Annotated[TrainingDayUpdate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        return await workout_service.update_training_day(
            workout_id=workout_id,
            training_day_id=training_day_id,
            data=data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.patch(
    "/workouts/{workout_id}/{training_day_id}/day_exercise/{exercise_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_day_exercise(
    workout_id: IntPath,
    training_day_id: IntPath,
    exercise_id: IntPath,
    data: Annotated[DayExerciseUpdate, Body()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        return await workout_service.update_day_exercise(
           workout_id=workout_id,
           training_day_id=training_day_id,
           exercise_id=exercise_id,
           data=data
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))
    except DataNotModified as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete(
    "/workouts/{workout_id}",
    status_code=HTTP_200_OK
)
async def delete_workout(
    workout_id: Annotated[int, Path()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        await workout_service.delete_workout(workout_id=workout_id)
        return Response(status_code=status.HTTP_200_OK)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete(
    "/workouts/{workout_id}/{training_day_id}",
    status_code=HTTP_200_OK
)
async def delete_training_day(
    workout_id: Annotated[int, Path()],
    training_day_id: Annotated[int, Path()],
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        await workout_service.delete_training_day(
            workout_id=workout_id,
            training_day_id=training_day_id
        )
        return Response(status_code=status.HTTP_200_OK)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete(
    "/workouts/{workout_id}/{training_day_id}/{exercise_id}",
    status_code=HTTP_200_OK
)
async def delete_day_exercise(
    workout_id: IntPath,
    training_day_id: IntPath,
    exercise_id: IntPath,
    workout_service: Annotated[WorkoutService, Depends(get_workout_service)]
):
    try:
        await workout_service.delete_day_exercise(
            workout_id=workout_id,
            training_day_id=training_day_id,
            exercise_id=exercise_id
        )
        return Response(status_code=status.HTTP_200_OK)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
        
