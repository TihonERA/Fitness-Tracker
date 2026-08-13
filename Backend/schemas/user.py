from uuid import UUID

from pydantic import BaseModel
from .base import BaseResponse, Str100, StrText, Password

from enum import StrEnum

class UserBase(BaseModel):
    login: Str100
    email: StrText

class UserResponse(BaseResponse, UserBase):
    id: UUID

class UserCreate(UserBase):
    password: Password

class UserCreateDB(UserBase):
    hash_password: str

class UserUpdate(BaseModel):
    login: Str100 | None = None
    email: StrText | None = None
    password: Password | None = None

class UserUpdateDTO(BaseModel):
    login: str | None = None
    email: str | None = None
    hash_password: str | None = None

class UserCachePrefixes(StrEnum):
    user_by_id = "user:by_id"
    user_by_login = "user:login"
    user_by_email = "user:email"
