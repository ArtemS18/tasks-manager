import logging
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
import pytest_asyncio
from httpx import ASGITransport, AsyncClient, Response
import pytest

from app.web.config import BaseConfig, setup_config

loggeer = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config()->BaseConfig:
    loggeer.info("Setup config")
    return setup_config('env/.test.env')


@pytest.fixture(scope="function")
def test_app(config: BaseConfig)->FastAPI:
    from app.web.app import setup_app
    loggeer.info("Setup app")
    return setup_app()

@pytest_asyncio.fixture(scope="function")
async def client(test_app: FastAPI):
    transport = ASGITransport(app=test_app)
    async with LifespanManager(test_app):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac





