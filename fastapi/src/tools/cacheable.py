import json


def cacheable(prefix: str = '', cache_expire: int = 300):
    def inner_wrapper(func):
        async def wrapper(*args, **kwargs):
            redis = args[0].redis
            data = await func(*args, **kwargs)
            if not data:
                return None
            if isinstance(data, list):
                key = f'{prefix}: {args[0].key}' if 'key' in dir(args[0]) else prefix
                await redis.set(key, json.dumps([item.json() for item in data]),
                                expire=cache_expire)
            else:
                await redis.set(f'{prefix}: {args[1]}', data.json(), expire=cache_expire)
            return data
        return wrapper
    return inner_wrapper
