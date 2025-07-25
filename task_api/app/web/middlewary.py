import logging
import typing
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import time

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


async def time_middlewary(request: "Request", call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    time_executing = time.perf_counter() - start

    logger.info(
        "All execution time %s : %.2f ms", request.url.path, time_executing * 1000
    )
    return response


def setup_middlewary(app: "FastAPI"):
    app.middleware("http")(time_middlewary)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
    Instrumentator().instrument(app).expose(app, include_in_schema=False)
