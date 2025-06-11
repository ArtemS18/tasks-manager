from fastapi import FastAPI
import pytest
from app.web.config import get_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

@pytest.fixture
def engin(test_app: FastAPI) -> AsyncEngine:
    config = get_config()
    engine = create_async_engine(config.DATABASE_URL, echo=config.ECHO)
    return engine


def session(engin: AsyncEngine):
    pass


