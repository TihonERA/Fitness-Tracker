from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from Backend.api.deps import GetCurrentUserDepends, UUIDPath, UserServiceDepends
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
    user_service: UserServiceDepends
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
    user_service: UserServiceDepends
):
    return await user_service.get_user_by_id(
        user_id=user_id
    )

@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: GetCurrentUserDepends,
    data: Annotated[UserUpdate, Body()],
    user_service: UserServiceDepends
):
    return await user_service.update_user(
        user_id=user_id,
        data=data
    )

@router.delete(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user_id: GetCurrentUserDepends,
    user_service: UserServiceDepends
):
    return await user_service.delete_user(
        user_id=user_id
    )
