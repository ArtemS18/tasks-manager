from fastapi import FastAPI

from app.api.routers import setup_routers
from app.bd.connection import setup_database

_app = FastAPI()

def setup_app() -> FastAPI:
    setup_database()
    setup_routers(_app)
    return _app
