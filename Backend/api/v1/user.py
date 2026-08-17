from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from Backend.api.deps import GetCurrentUserDepends, UUIDPath, UserProxyDepends
from Backend.schemas.user import UserResponse, UserUpdate

router = APIRouter(
    tags=["User Table Endpoints"],
    prefix="/users"
)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_current_user(
    user_id: GetCurrentUserDepends,
    user_service: UserProxyDepends
):
    return await user_service.get_user_by_id(
        user_id=user_id
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: UUIDPath,
    user_service: UserProxyDepends
):
    return await user_service.get_user_by_id(
        user_id=user_id
    )

@router.delete(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user_id: GetCurrentUserDepends,
    user_service: UserProxyDepends
):
    return await user_service.delete_user(
        user_id=user_id
    )
