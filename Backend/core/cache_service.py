from datetime import timedelta
from typing import Any, Literal

from redis.asyncio import Redis
from redis.typing import EncodableT

class CacheService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get(
        self,
        key: str
    ) -> bytes | str | None:
        return await self.redis.get(key)

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

    def _return_formated_cache_parts(
        self,
        data: dict[str, Any]
    ):
        parts = []
        for key, value in sorted(data.items()):
            if isinstance(value, dict):
                nested_parts = self._return_formated_cache_parts(value)
                parts.extend(nested_parts)
            else:
                parts.append(f"{key.replace(' ', '')}={value}")

        return parts

    async def delete_searching_with_pattern(
        self,
        prefix: str,
        **identifiers: Any
    ) -> None:
        cache_parts = self._return_formated_cache_parts(data=identifiers)

        pattern = f"{prefix}:*{'*'.join(cache_parts)}*"
        cache_keys = [key async for key in self.redis.scan_iter(match=pattern, count=10)]

        if cache_keys:
            await self.redis.delete(*cache_keys)

    def formate_key(
        self,
        prefix: str,
        **identifiers
    ) -> str:
        cache_parts = self._return_formated_cache_parts(data=identifiers)

        return f"{prefix}:{':'.join(cache_parts)}"
             
