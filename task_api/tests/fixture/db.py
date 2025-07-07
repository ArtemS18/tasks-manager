import pytest
import pytest_asyncio
from sqlalchemy import Engine, NullPool, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from app.web.config import BaseConfig


@pytest.fixture(scope="session")
def session_manager(engin: AsyncEngine):
    session = async_sessionmaker(engin)
    return session


@pytest.fixture(scope="session")
def sync_engine(config: BaseConfig):
    sync_url = config.db.url.replace("+asyncpg", "")
    engine = create_engine(sync_url, echo=config.db.echo, poolclass=NullPool)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_schema(sync_engine: Engine):
    from app.store.bd import models
    from app.base.base_model import Base

    schema = "test_schema"
    print("SETUP_SCHEMA CALLED")

    for table in Base.metadata.tables.values():
        table.schema = schema

    with sync_engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
        conn.execute(text(f"CREATE SCHEMA {schema}"))
        Base.metadata.create_all(bind=conn)

    yield
    # await asyncio.sleep(30)

    print("DROP SCHEMA CALLED")
    with sync_engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))

    for table in Base.metadata.tables.values():
        table.schema = "public"

    sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def engine(config: BaseConfig, setup_schema):
    engine = create_async_engine(config.db.url, echo=config.db.echo)
    yield engine
    await engine.dispose()
