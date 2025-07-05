import functools
import logging
from time import perf_counter
from typing import Any, Callable
from app.entity.base import Base

logger = logging.getLogger("web")

def json_response(schema: Base, obj: Any):
    return schema.model_validate(obj).model_dump()

def async_time(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        t0 = perf_counter()
        res = await func(*args, **kwargs)
        logger.debug(f"async {func.__name__} execuded:  {perf_counter() - t0}")
        return res
    return wrapper
