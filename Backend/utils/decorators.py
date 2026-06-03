from functools import wraps
import hashlib
import json
from typing import Type, Union
from pydantic import TypeAdapter, BaseModel
from datetime import timedelta

def cache(expire: Union[int, timedelta], response_model: Type[BaseModel]):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            redis_client = self.redis
            args_json = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
            arguments_hash = hashlib.md5(args_json.encode()).hexdigest()
            key = f"{func.__module__}:{func.__name__}:{arguments_hash}"
            cached_data = redis_client.get(key)
            if cached_data:
                return response_model.model_validate_json(cached_data)
            result = await func(self, *args, **kwargs)
            if result:
                adapter = TypeAdapter(response_model)
                result_json = adapter.dump_json(result).decode("utf-8")
                redis_client.set(key, value=result_json, ex=expire)
            return result
        return wrapper
    return decorator


