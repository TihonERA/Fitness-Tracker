from pydantic import BaseModel

from Backend.schemas.base import StrText, Password

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class TokenResponse(BaseModel):
    token: str 
    token_type: str

class UserAuthorize(BaseModel):
    login_or_email: StrText
    password: Password
