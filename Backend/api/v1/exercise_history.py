from typing import Annotated

from fastapi import APIRouter, Body, Query

from Backend.api.deps import ExHistoryProxyDepends, GetCurrentUserDepends, IntPath
from Backend.schemas.exercise_history import (
    ExerciseHistoryCreate,
    ExerciseHistoryGetAll,
    ExerciseHistoryRelalationsResponse,
    ExerciseHistoryResponse,
    ListExerciseHistoryResponse,
)

router = APIRouter(prefix="/exercise_history", tags=["ExerciseHistory Table Endpoints"])


@router.get("all")
async def get_all_exercise_history(
    user_id: GetCurrentUserDepends,
    data: Annotated[ExerciseHistoryGetAll, Query()],
    proxy: ExHistoryProxyDepends,
) -> ListExerciseHistoryResponse:
    return await proxy.get_all_exercise_history(user_id, data)


@router.get("/{exercise_history_id}")
async def get_exercise_history(
    user_id: GetCurrentUserDepends, history_id: IntPath, proxy: ExHistoryProxyDepends
) -> ExerciseHistoryRelalationsResponse:
    return await proxy.get_exercise_history(user_id, history_id)


@router.post("/")
async def create_exercise_history(
    user_id: GetCurrentUserDepends,
    data: Annotated[ExerciseHistoryCreate, Body()],
    proxy: ExHistoryProxyDepends,
) -> ExerciseHistoryRelalationsResponse:
    return await proxy.create_exercise_history(user_id, data)


@router.delete("/{exercise_history_id}")
async def delete_history(
    user_id: GetCurrentUserDepends, history_id: IntPath, proxy: ExHistoryProxyDepends
) -> ExerciseHistoryResponse:
    return await proxy.delete_history(user_id, history_id)
