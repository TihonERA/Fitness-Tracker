from datetime import timedelta
from typing import Any, Awaitable, Callable, Generic, cast

from redis.asyncio import Redis
from redis.typing import EncodableT

from pydantic import BaseModel

class CacheBaseProxy:
    def __init__(self, redis: Redis, scheme: type[BaseModel]) -> None:
        self.redis = redis
        self.scheme = scheme

    async def _wrap_cache(
        self,
        key: str,
        db_func: Callable[[], Awaitable[Any]],
        response_model: type[BaseModel] | None = None
    ) -> str:
        if data := await self.get(key):
            return data

        db_data = await db_func()

        if response_model:
            validated_db_data = response_model.model_validate(db_data)
        else:
            validated_db_data = self.scheme.model_validate(db_data)

        db_data_json = validated_db_data.model_dump_json()

        await self.set(
            key=key,
            value=db_data_json
        )

        return db_data_json

    async def get(
        self,
        key: str
    ) -> str | None:
        return cast(str, await self.redis.get(key))

    async def set(
        self,
        key: str,
        value: EncodableT,
        expire: timedelta= timedelta(hours=12)
    ) -> None:
        await self.redis.set(
            name=key,
            value=value,
            ex=expire
        )
