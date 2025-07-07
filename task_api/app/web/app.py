from app.api.routers import setup_routers
from app.lib.fastapi import FastAPI
from app.web.config import get_app_config
from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.middlewary import setup_middlewary

from app.store import setup_store

_app = FastAPI(lifespan=lifespan)


def setup_app() -> FastAPI:
    get_app_config(_app)
    setup_store(_app)
    setup_logger(_app)
    setup_middlewary(_app)
    setup_routers(_app)
    return _app
