from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from Backend.schemas.auth import TokenPair, UserAuthorize
from Backend.schemas.user import UserCreate, UserCreateDB
from Backend.utils.validators import InvalidCredentials, NotFound

from ..core.config import settings

import jwt
from pwdlib import PasswordHash

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.services.UserService import UserService


class AuthService:

    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis
        self.userservice = UserService(session=session, redis=redis)
        self.password_hash = PasswordHash.recommended()
        self.DUMMYHASH = "dummy_hash_for_safety_YYYYYYYYYYYYYYYYYYYYYYY"
        
    async def register(self, data: UserCreate) -> TokenPair:
        user = await self.userservice.check_if_user_exists(
            login=data.login,
            email=data.email
        )
        if user:
            if user.login == data.login:
                raise InvalidCredentials(detail="Login is already taken")
            elif user.email == data.email:
                raise InvalidCredentials(detail="Email is already taken")
            else:
                raise InvalidCredentials(detail="Both login and email are already taken")

        hash_password = self.password_hash.hash(data.password)
        user_scheme_db = UserCreateDB(
            login=data.login,
            email=data.email,
            hash_password=hash_password
        )

        user = await self.userservice.create_user(
            data=user_scheme_db
        )
        tokens = await self._create_token_pair(user_id=user.user_id)
        return tokens

    async def login(self, data: UserAuthorize) -> TokenPair:
        try:
            if '@' in data.login_or_email and '.' in data.login_or_email:
                user = await self.userservice.get_user_by_email(
                    email=data.login_or_email
                )
            else:
                user = await self.userservice.get_user_by_login(
                    login=data.login_or_email
                 )
            if not self.password_hash.verify(
                 data.password,
                 user.hash_password
            ):
                self.password_hash.verify(
                    self.DUMMYHASH,
                    user.hash_password
                )
                raise InvalidCredentials(detail="Invalid password") 

            tokens = await self._create_token_pair(user_id=user.user_id)
            return tokens
        except NotFound:
            self.password_hash.verify(
                self.DUMMYHASH,
                self.password_hash.hash(self.DUMMYHASH)
            )
            raise InvalidCredentials(detail="Invalid login or email")

    def get_current_user(self, token: str | bytes) -> UUID:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            return self._get_user_id_from_payload(payload=payload)
        except jwt.PyJWTError:
            raise InvalidCredentials(detail="Invalid token")

    def _get_user_id_from_payload(self, payload: dict[str, Any]) -> UUID:
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidCredentials(detail="Invalid token")
        return UUID(user_id)

    async def refresh(self, token: str | bytes | None) -> TokenPair:
        if token is None:
            raise InvalidCredentials(detail="Invalid Token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user_id= self._get_user_id_from_payload(payload=payload)
            token_pair = await self._create_token_pair(user_id=user_id)
            return token_pair
        except jwt.PyJWTError:
            raise InvalidCredentials(detail="Invalid token")

    def _create_token(self, data: dict, expire: timedelta) -> str:
        to_encode = data.copy()
        token_expire = datetime.now(timezone.utc) + expire
        to_encode.update({"exp": token_expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def _create_token_pair(self, user_id: UUID) -> TokenPair:
        user_id_str = str(user_id)

        access_token_data = {"sub": user_id_str, "type": "bearer"}
        access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = self._create_token(
            data=access_token_data,
            expire=access_token_expire
        )

        refresh_token_data = {"sub": user_id_str, "type": "refresh"}
        refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        refresh_token = self._create_token(
            data=refresh_token_data,
            expire=refresh_token_expire
        )
        refresh_token_ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        await self.redis.set(
            name=self._refrest_token_key(user_id=user_id_str, token=refresh_token),
            value=refresh_token, 
            ex=refresh_token_ttl
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def _refrest_token_key(user_id, token: str) -> str:
        return f"{user_id}:{token}"
        

