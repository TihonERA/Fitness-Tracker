from fastapi import APIRouter, Depends, Response, status, HTTPException, Body
from typing import Annotated
from uuid import UUID
from pydantic import ValidationError
from starlette.status import HTTP_200_OK
from Backend.tasks.muscle_rates import get_muscle_contribution_list, get_muscles_balance
from ...schemas.workout import DayExerciseCreate, DayExerciseUpdate, TrainingDayCreate, TrainingDayUpdate, WorkoutCreate, WorkoutResponse, WorkoutGetAllFilter, WorkoutUpdate
from ...utils.validators import DataNotModified, NotFound
from ..deps import WorkoutServiceDepends, get_workouts_filter, IntPath

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
    user_id: UUID,
    filter: Annotated[WorkoutGetAllFilter, Depends(get_workouts_filter)],
    workout_service: WorkoutServiceDepends
):
    return await workout_service.get_all_workouts(
        filter=filter,
        user_id=user_id
    )

@router.get(
    "/{workout_id}",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK      
)
async def get_workout(
    workout_id: IntPath, 
    workout_service: WorkoutServiceDepends,
):
    try:
        return await workout_service.get_workout(workout_id)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

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
    "/workout_schedule", 
    response_model=WorkoutResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_workout_with_schedule(
    data: Annotated[WorkoutCreate, Body()],
    workout_service: WorkoutServiceDepends
):
    return await workout_service.create_workout_with_schedule(data)

@router.post(
    "/{workout_id}/training_day",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK
)
async def create_training_day_in_workout(
    workout_id: IntPath,
    data: Annotated[TrainingDayCreate, Body()],
    workout_service: WorkoutServiceDepends
):
    try:
        return await workout_service.create_training_day(
            workout_id=workout_id,
            data=data 
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors(include_url=False))

@router.post(
    "/{workout_id}/{training_day_id}/day_exercise",
    response_model=WorkoutResponse,
    status_code=status.HTTP_200_OK
)
async def create_day_exercise_in_training_day(
    workout_id: IntPath,
    training_day_id: IntPath,
    data: Annotated[DayExerciseCreate, Body()],
    workout_service: WorkoutServiceDepends
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
    "/{workout_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_workout(
    workout_id: IntPath,
    data: Annotated[WorkoutUpdate, Body()],
    workout_service: WorkoutServiceDepends
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
    "/{workout_id}/training_day/{training_day_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_training_days_in_workout(
    workout_id: IntPath,
    training_day_id: IntPath,
    data: Annotated[TrainingDayUpdate, Body()],
    workout_service: WorkoutServiceDepends
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
    "/{workout_id}/{training_day_id}/day_exercise/{exercise_id}",
    response_model=WorkoutResponse,
    status_code=HTTP_200_OK
)
async def update_day_exercise(
    workout_id: IntPath,
    training_day_id: IntPath,
    exercise_id: IntPath,
    data: Annotated[DayExerciseUpdate, Body()],
    workout_service: WorkoutServiceDepends
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
    "/{workout_id}",
    status_code=HTTP_200_OK
)
async def delete_workout(
    workout_id: IntPath,
    workout_service: WorkoutServiceDepends
):
    try:
        await workout_service.delete_workout(workout_id=workout_id)
        return Response(status_code=status.HTTP_200_OK)
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete(
    "/{workout_id}/{training_day_id}",
    status_code=HTTP_200_OK
)
async def delete_training_day(
    workout_id: IntPath,
    training_day_id: IntPath,
    workout_service: WorkoutServiceDepends
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
    "/{workout_id}/{training_day_id}/{exercise_id}",
    status_code=HTTP_200_OK
)
async def delete_day_exercise(
    workout_id: IntPath,
    training_day_id: IntPath,
    exercise_id: IntPath,
    workout_service: WorkoutServiceDepends
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
        
