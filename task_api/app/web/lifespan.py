from contextlib import asynccontextmanager
import typing

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    await app.store.connect_all()
    yield
    await app.store.disconnect_all()
