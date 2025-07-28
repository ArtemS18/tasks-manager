from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import config

engin = create_async_engine(url=config.DATABASE_URL, poolclass=NullPool)
