import logging
import typing
from fastapi import Response
from prometheus_fastapi_instrumentator import Instrumentator

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


async def exeption_middlewary(request: "Request", call_next):
    try:
        response: Response = await call_next(request)
        return response
    except Exception as e:
        logger.error(e)


def setup_middlewary(app: "FastAPI"):
    Instrumentator().instrument(app).expose(app, include_in_schema=False)
    # app.middleware('http')(exeption_middlewary)
