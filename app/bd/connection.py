from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from app.web.config import get_config


_engine: AsyncEngine = None
_session: async_sessionmaker[AsyncSession] = None

def setup_database():
    global _engine, _session
    config = get_config()
    
    if _engine is None:
        _engine = create_async_engine(config.DATABASE_URL, echo=config.ECHO)
    if _session is None:
        _session = async_sessionmaker(_engine, expire_on_commit=False)

def get_session() -> async_sessionmaker[AsyncSession]:
    if _session is None:
        raise RuntimeError("Session is not initialized")
    return _session