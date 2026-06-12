from functools import wraps
from typing import Type, Union, Any, Tuple, Dict
from pydantic import BaseModel
from datetime import timedelta

def cache(expire: Union[int, timedelta], response_model: Union[Type[BaseModel], Any], prefix: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            redis_client = self.redis
            
            pk = _extract_primary_key(args, kwargs)

            cache_key = f"{prefix}:{pk}"

            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return response_model.model_validate_json(cached_data) 
            
            result = await func(self, *args, **kwargs)
            if result:
                result_json = result.model_dump_json() 
                await redis_client.set(name=cache_key, value=result_json, ex=expire)

            return result
        return wrapper
    return decorator

def _extract_primary_key(
    args: Tuple[Any],
    kwargs: Dict[str, Any]
) -> int | str | None:
    for key, value in kwargs.items():
        if key.endswith("id"):
            return value
    
    if args:
        return args[0]


