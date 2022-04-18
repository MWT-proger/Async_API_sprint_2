import json


def cacheable(cache_expire: int = 300):
    def inner_wrapper(func):
        async def wrapper(*args, **kwargs):
            redis = args[0].redis
            prefix = args[0].index
            data = await func(*args, **kwargs)
            key = args[0].key
            if not data:
                return None
            if isinstance(data, list):
                key = f'{prefix}: {key}' if key else prefix
                await redis.set(key, json.dumps([item.json() for item in data]),
                                expire=cache_expire)
            else:
                await redis.set(f'{prefix}: {args[1]}', data.json(), expire=cache_expire)
            return data
        return wrapper
    return inner_wrapper
