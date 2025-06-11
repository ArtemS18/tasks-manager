from fastapi import FastAPI
import pytest_asyncio
from app.web.app import setup_app
from app.web.config import setup_config, get_config
from httpx import ASGITransport, AsyncClient
import pytest

@pytest.fixture(scope="session")
def test_app()->FastAPI:
    setup_config('tests/.env')
    return setup_app()

@pytest_asyncio.fixture(scope="session")
async def async_client(test_app: FastAPI):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

