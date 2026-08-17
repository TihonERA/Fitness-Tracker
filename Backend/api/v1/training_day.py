from typing import Annotated

from fastapi import APIRouter, Body, status

from Backend.api.deps import GetCurrentUserDepends, IntPath, TrainingDayProxyDepends
from Backend.schemas.training_day import TrainingDayCreate, TrainingDayResponse, TrainingDayUpdate

router = APIRouter(
    tags=["TrainingDay Tables Endpoints"],
    prefix="/training_days"
)

@router.post(
    "/{workout_id}",
    status_code=status.HTTP_201_CREATED
)
async def create_training_day_in_workout(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    data: Annotated[TrainingDayCreate, Body()],
    td_proxy: TrainingDayProxyDepends
) -> TrainingDayResponse:
    return await td_proxy.create_training_day(
        user_id=user_id,
        workout_id=workout_id,
        data=data
    )

@router.patch(
    "/{workout_id}/{day_id}",
    status_code=status.HTTP_200_OK
)
async def update_training_day(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    data: Annotated[TrainingDayUpdate, Body()],
    td_proxy: TrainingDayProxyDepends
) -> TrainingDayResponse:
    return await td_proxy.update_training_day(
        user_id=user_id,
        workout_id=workout_id,
        day_id=day_id,
        data=data
    )

@router.delete(
    "/{workout_id}/{day_id}",
    status_code=status.HTTP_200_OK
)
async def delete_training_day(
    user_id: GetCurrentUserDepends,
    workout_id: IntPath,
    day_id: IntPath,
    td_proxy: TrainingDayProxyDepends
) -> TrainingDayResponse:
    return await td_proxy.delete_training_day(user_id=user_id,
        workout_id=workout_id,
        day_id=day_id
    )
