from typing import Annotated

from fastapi import APIRouter, Body, Query

from Backend.api.deps import GetCurrentUserDepends, IntPath, TrDayHistoryProxyDepends
from Backend.schemas.AnalyticsHistory import CreateHistory, HistoryResponse
from Backend.schemas.training_day_history import (
    ListTrDayHistoryResponse,
    TrainingDayHistoryGetAll,
    TrainingDayHistoryResponse,
    TrainingDayRelationHistoryResponse,
)

router = APIRouter(
    prefix="/training_day_history", tags=["TrainingDayHistory Table Endpoints"]
)


@router.get("/all")
async def get_all_tr_day_history(
    user_id: GetCurrentUserDepends,
    data: Annotated[TrainingDayHistoryGetAll, Query()],
    proxy: TrDayHistoryProxyDepends,
) -> ListTrDayHistoryResponse:
    return await proxy.get_all_tr_day_history(user_id=user_id, data=data)


@router.get("/{history_id}")
async def get_tr_day_history(
    user_id: GetCurrentUserDepends, history_id: IntPath, proxy: TrDayHistoryProxyDepends
) -> TrainingDayRelationHistoryResponse:
    return await proxy.get_loaded_tr_day_history(user_id=user_id, history_id=history_id)


@router.post("/")
async def create_history(
    user_id: GetCurrentUserDepends,
    data: Annotated[CreateHistory, Body()],
    proxy: TrDayHistoryProxyDepends,
) -> HistoryResponse:
    return await proxy.create_history(user_id=user_id, data=data)


@router.delete("/{history_id}")
async def delete_history(
    user_id: GetCurrentUserDepends, history_id: IntPath, proxy: TrDayHistoryProxyDepends
) -> TrainingDayHistoryResponse:
    return await proxy.delete_history(user_id=user_id, history_id=history_id)
