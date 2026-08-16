from datetime import timedelta
from typing import Any, Awaitable, Callable, Generic, TypeVar, cast, overload

from redis.asyncio import Redis
from redis.typing import EncodableT

from pydantic import BaseModel

class BaseCacheProxy[SchemeT: BaseModel]:
    def __init__(self, redis: Redis, scheme: type[SchemeT]) -> None:
        self.redis = redis
        self.scheme = scheme

    @overload
    async def _wrap_cache(
        self,
        key: str,
        db_func: Callable[[], Awaitable[Any]],
        response_model: None = None
    ) -> SchemeT: ...

    @overload
    async def _wrap_cache[M: BaseModel](
        self,
        key: str,
        db_func: Callable[[], Awaitable[Any]],
        response_model: type[M]
    ) -> M: ...

    async def _wrap_cache(
        self,
        key: str,
        db_func: Callable[[], Awaitable[Any]],
        response_model: type[BaseModel] | None = None
    ) -> Any:
        model = response_model or self.scheme

        if data := await self.get(key):
            return model.model_validate_json(data)

        db_data = await db_func()

        validated_db_data = model.model_validate(db_data)

        db_data_json = validated_db_data.model_dump_json()

        await self.set(
            key=key,
            value=db_data_json
        )

        return validated_db_data

    async def get(
        self,
        key: str
    ) -> str | None:
        return cast(str, await self.redis.get(key))

    async def set(
        self,
        key: str,
        value: EncodableT,
        expire: timedelta = timedelta(hours=12)
    ) -> None:
        await self.redis.set(
            name=key,
            value=value,
            ex=expire
        )

    async def sadd(
        self,
        key: str,
        values: list[str] | str,
        expire: timedelta = timedelta(hours=12)
    ) -> None:
        if isinstance(values, list):
            await self.redis.sadd(key, *values)
        else:
            await self.redis.sadd(key, values)
        await self.redis.expire(key, expire)
