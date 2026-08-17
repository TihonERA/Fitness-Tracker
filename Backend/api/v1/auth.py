from typing import Annotated

from fastapi import Body, Cookie, APIRouter, HTTPException, Response, status

from Backend.api.deps import AuthServiceDepends, GetCurrentUserDepends
from Backend.schemas.auth import UserAuthorize
from Backend.schemas.user import UserCreate, UserUpdate

router = APIRouter(
   tags=["Authorization Endpoints"],
   prefix="/auth"
)

def set_access_and_refresh_cookie(
    response: Response,
    access_token: str,
    refresh_token: str
):
    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        secure=True,
        samesite='lax',
        httponly=True,
    )

@router.post(
    "/users",
    status_code=status.HTTP_200_OK
)
async def register(
    data: Annotated[UserCreate, Body()],
    auth_service: AuthServiceDepends,
    response: Response
):
    tokens = await auth_service.register(data=data)

    set_access_and_refresh_cookie(
        response=response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token
    )
    return {"status": "success"}

@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login(
    data: Annotated[UserAuthorize, Body()],
    auth_service: AuthServiceDepends,
    response: Response
):
    tokens = await auth_service.login(data=data)
    
    set_access_and_refresh_cookie(
        response=response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token
    )
    return {"status": "success"}

@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK
)
async def refresh(
    auth_service: AuthServiceDepends,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    tokens = await auth_service.refresh(token=refresh_token)

    set_access_and_refresh_cookie(
        response=response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token
    )
    return status.HTTP_200_OK

@router.patch(
    "/me",
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: GetCurrentUserDepends,
    data: Annotated[UserUpdate, Body()],
    auth_service: AuthServiceDepends
):
    return await auth_service.update_user(
        user_id=user_id,
        data=data
    )

