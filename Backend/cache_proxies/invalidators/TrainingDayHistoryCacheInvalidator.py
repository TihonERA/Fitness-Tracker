import asyncio
import logging

from uuid import UUID

from redis import RedisError
from redis.asyncio import Redis

import json

from Backend.cache_proxies.invalidators.BaseCacheInvalidator import BaseCacheInvalidator
from Backend.cache_proxies.key_formatters.TrainingDayHistoryCacheKeyFormatter import (
    TrainingDayHistoryCacheKeyFormatter,
)

logger = logging.getLogger(__name__)


class TrainingDayHistoryCacheInvalidator(
    BaseCacheInvalidator[TrainingDayHistoryCacheKeyFormatter]
):
    def __init__(
        self, redis: Redis, formatter: TrainingDayHistoryCacheKeyFormatter
    ) -> None:
        super().__init__(redis, formatter)

    async def invalidate_loaded(self, id: int) -> None:
        loaded_key = self.formatter.get_loaded_key(id)

        await self.redis.delete(loaded_key)

    async def invalidate_get_all(self, user_id: UUID) -> None:
        version_key = self.formatter.get_version_key(user_id)

        await self.redis.incr(version_key)

    async def invalidate_all(self, user_id: UUID, id: int) -> None:
        tag_key = self.formatter.get_tag_key(user_id)
        loaded_key = self.formatter.get_loaded_key(id)
        version_key = self.formatter.get_version_key(user_id)

        max_attempts = 3
        delay = 0.2

        for attempt in range(max_attempts):
            try:
                async with self.redis.pipeline(transaction=True) as pipe:
                    pipe.delete(loaded_key)
                    pipe.srem(tag_key, loaded_key)
                    pipe.incr(version_key)

                    await pipe.execute()

                return
            except RedisError as e:
                # attempt + 1 нужен для показа реального номера попытки, потому что отсчет начинается с 0 до 2
                logger.warning(
                    f"Попытка {attempt+1}/{max_attempts} инвалидации кеша пользователя {user_id} провалилась: {e}"
                )
                await asyncio.sleep(delay * (2 ** (attempt)))

        logger.critical(
            f"Критическая ошибка: Не удалось инвалидировать кеш для пользователя {user_id} после {max_attempts} попыток"
            f"Данные рассинхронизированы"
        )

        raise RuntimeError("Cache invalidation failed down stream")
