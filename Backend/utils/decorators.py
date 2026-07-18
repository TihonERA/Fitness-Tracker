from functools import wraps
from typing import Union, Any, Tuple, Dict
from datetime import timedelta
from pydantic import BaseModel
from sqlalchemy.orm import InstrumentedAttribute
from ..utils.validators import NotFound, InternalServerError
import logging

logger = logging.getLogger(__name__)

def cache(ttl: Union[int, timedelta], column: InstrumentedAttribute, schema: type[BaseModel]):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            redis_client = self.redis
            
            pk = _extract_primary_key(args, kwargs)

            cache_key = f"{column.key}:{pk}"

            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return schema.model_validate_json(cached_data) 
            try:
                result = await func(self, *args, **kwargs)
            except NotFound:
                raise
            if result:
                result_json = schema.model_validate(result).model_dump_json()
                await redis_client.set(name=cache_key, value=result_json, ex=ttl)

            return result
        return wrapper
    return decorator

def invalidate_cache(column: InstrumentedAttribute):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try: 
                result = await func(self, *args, **kwargs)
            except NotFound:
                raise

            redis = self.redis
            attr_name = column.key

            if not hasattr(result, attr_name):
                print(f"{result}\t{attr_name}")
                raise InternalServerError()
 
            pk = getattr(result, attr_name)
            cache_key = f"{attr_name}:{pk}"

            await redis.delete(cache_key)
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


