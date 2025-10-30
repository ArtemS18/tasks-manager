import functools
import logging
import importlib
from time import perf_counter
from typing import Any, Callable
from app.base.base_pydantic import Base
from fastapi import HTTPException, Response, status

logger = logging.getLogger("web")


def json_response(schema: Base, obj: Any):
    return schema.model_validate(obj).model_dump()


def async_time(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        t0 = perf_counter()
        res = await func(*args, **kwargs)
        time_ex = round((perf_counter() - t0) * 1000, 2)
        logger.info(f"{func.__qualname__} execuded: {time_ex}")
        return res

    return wrapper  # type: ignore


def set_cookie(
    response: Response,
    key: str,
    value: str,
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=60 * 60 * 24,
    path="/",
):
    response.set_cookie(
        key=key,
        value=value,
        httponly=httponly,
        secure=secure,
        samesite=samesite,
        max_age=max_age,
        path=path,
    )
    return response


def import_obj(path: str):
    if path.count(":") != 1:
        raise ValueError(f"Not found ':' in path or count ':' more one: {path}")

    modul_path, obj = path.split(":", 1)
    module = importlib.import_module(modul_path)

    return getattr(module, obj)
