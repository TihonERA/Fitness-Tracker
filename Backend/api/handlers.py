from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse
from ..utils.exceptions import *

router = APIRouter()

def not_found_handler(request: Request, exc: Exception):
    assert isinstance(exc, NotFound)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

def internal_server_error_handler(request: Request, exc: Exception):
    assert isinstance(exc, InternalServerError)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

def invalid_credentials_handler(request: Request, exc: Exception):
    assert isinstance(exc, InvalidCredentials)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
