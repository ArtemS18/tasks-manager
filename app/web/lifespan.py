from contextlib import asynccontextmanager
import typing

from app.store.broker.connect import (
    connect as pica_connect, 
    disconnect as pica_disconnect
)
from app.store.broker.email.connect import (
    connect as smtp_connect, 
    disconnect as smtp_disconnect
)
if typing.TYPE_CHECKING:
    from app.web.app import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    await app.store.user.connect()
    await app.store.task.connect()
    await smtp_connect()
    await pica_connect()
    yield
    await pica_disconnect()
    await smtp_disconnect()
    await app.store.user.disconnect()
    await app.store.task.disconnect()
