from fastapi import FastAPI

from app.api.routers import setup_routers
from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.middlewary import setup_middlewary

_app = FastAPI(lifespan=lifespan)

def setup_app() -> FastAPI:
    setup_logger(__name__)
    setup_middlewary(_app)
    setup_routers(_app)
    return _app
