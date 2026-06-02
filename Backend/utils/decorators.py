from functools import wraps
from pydantic import TypeAdapter
from datetime import timedelta

def cache(expire: int | timedelta, response_model: object):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, data: object):
            redis_client = self.redis

            fields = data.model_dump()
            pk = None
            for field_name, field_value in fields.items():
                if field_name.endswith("_id"):
                    pk = field_value
                    break
            if pk is None:
                pk = data
            key = f"{func.__name__}:{pk}"
            cached_data = redis_client.get(key)
            if cached_data:
                adapter = TypeAdapter(response_model)
                return adapter.validate_json(cached_data)
            result = await func(self, data)
            if result:
                adapter = TypeAdapter(response_model)
                result_json = adapter.dump_json(result).decode("utf-8")
                redis_client.set(key, value=result_json, ex=expire)
            return result
        return wrapper
    return decorator


