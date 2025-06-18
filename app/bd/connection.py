import logging
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.web.config import get_config

logger = logging.getLogger(__name__)

_engine: AsyncEngine = None
_session: async_sessionmaker[AsyncSession] = None

async def ping(_session: async_sessionmaker[AsyncSession]):
    try:
        async with _session() as session:
            await session.execute(text('SELECT 1'))
        logger.info("Test request to database PASSED")
        return True
    except SQLAlchemyError as e:
        logger.error(e)
    return False
    

def connect():
    global _engine, _session
    config = get_config()
    
    if _engine is None:
        _engine = create_async_engine(config.DATABASE_URL, echo=config.ECHO)
    if _session is None:
        _session = async_sessionmaker(_engine, expire_on_commit=False)
        #if asyncio.run(ping(_session)):
        logger.info("Successed connection to pgsql database")
            #return _session
        #logger.warning('Failed connection to pgsql database')

def get_session() -> async_sessionmaker[AsyncSession]:
    if _session is None:
        raise RuntimeError("Session is not initialized")
    return _session

async def disconnect():
    global _engine, _session
    if _engine:
        _engine.dispose()
        _engine = None
        logger.info("Disconnect to pgsql database")
    if _session:
        _session = None