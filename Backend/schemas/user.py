from uuid import UUID

from pydantic import BaseModel
from .base import Str100, StrText, Password

class UserBase(BaseModel):
    login: Str100
    email: StrText

class UserResponse(UserBase):
    user_id: UUID

class UserCreate(UserBase):
    password: Password

class UserCreateDB(UserBase):
    hash_password: str

class UserUpdate(BaseModel):
    login: Str100 | None = None
    email: StrText | None = None
    password: Password | None = None
