from contextlib import asynccontextmanager
import typing

from app.broker.connect import (
    connect as pica_connect, 
    disconnect as pica_disconnect
)
if typing.TYPE_CHECKING:
    from app.web.app import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    await app.store.connect_all()
    await pica_connect()
    yield
    await pica_disconnect()
    await app.store.disconnect_all()
