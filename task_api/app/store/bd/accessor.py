import typing
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

class PgAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.engine: AsyncEngine| None = None
        self.session: async_sessionmaker[AsyncSession]| None = None

    async def connect(self):
        self.engine = create_async_engine(url=self.app.config.db.url, echo = self.app.config.db.echo)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
        self.session = None
