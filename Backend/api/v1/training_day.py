from typing import Annotated

from fastapi import APIRouter, Body, status

from Backend.api.deps import GetCurrentUserDepends, IntPath, TrainingDayServiceDepends
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayResponse, TrainingDayUpdate

router = APIRouter(
    tags=["TrainingDay Tables Endpoints"],
    prefix="/training_days"
)

@router.get(
    "/{workout_id}/{day_id}",
    response_model=TrainingDayResponse,
    status_code=status.HTTP_200_OK
)
async def get_training_day(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    trdayservice: TrainingDayServiceDepends
):
    return await trdayservice.get_training_day(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id
    )

@router.post(
    "/{workout_id}",
    response_model=TrainingDayResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_training_day_in_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    data: Annotated[TrainingDayCreate, Body()],
    trdayservice: TrainingDayServiceDepends
):
    return await trdayservice.create_training_day(
        user_id=user_id,
        workout_id=workout_id,
        data=data
    )

@router.patch(
    "/{workout_id}/{day_id}",
    response_model=TrainingDayResponse,
    status_code=status.HTTP_200_OK
)
async def update_training_day(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    data: Annotated[TrainingDayUpdate, Body()],
    trdayservice: TrainingDayServiceDepends
):
    return await trdayservice.update_training_day(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        data=data
    )

@router.delete(
    "/{workout_id}/{day_id}",
    response_model=TrainingDayResponse,
    status_code=status.HTTP_200_OK
)
async def delete_training_day(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    trdayservice: TrainingDayServiceDepends
):
    return await trdayservice.delete_training_day(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id
    )
