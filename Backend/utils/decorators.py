import asyncio
from functools import wraps
import inspect
from types import CoroutineType
from typing import Any, Callable
from logging import Logger

from redis import RedisError


def get_bound_args(func: Callable, *args, **kwargs) -> dict[str, Any]:
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments


def get_class_name(kwargs: dict[str, Any]) -> str | None:
    self_obj = kwargs.get("self", None)
    if not self_obj:
        return self_obj
    return self_obj.__class__.__name__


def cache_invalidation_logger(logger: Logger):
    def decorator[**P, R](
        func: Callable[P, CoroutineType[Any, Any, R]],
    ) -> Callable[P, CoroutineType[Any, Any, R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_args = get_bound_args(func, *args, **kwargs)

            user_id = bound_args.get(
                "user_id", "!!!Айди пользователя не было передано в функцию!!!"
            )
            class_name = get_class_name(bound_args)

            if class_name is None:
                logger.warning(
                    "Декоратор обёртывает функцию, которая находится не в классе"
                )

            max_attempts = 3
            delay = 0.2

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except RedisError as e:
                    logger.warning(
                        f"Попытка {attempt+1}/{max_attempts} инвалидации кеша пользователя {user_id} провалилась: {e}."
                        f"(В классе {class_name} функции {func.__name__})"
                    )
                    await asyncio.sleep(delay * (2**attempt))

            logger.critical(
                f"Критическая ошибка: Не удалось инвалидировать кеш для пользователя {user_id} после {max_attempts} попыток."
                f"Данные рассинхронизированы"
            )

            raise RuntimeError("Cache invalidation failed down stream")

        return wrapper

    return decorator
