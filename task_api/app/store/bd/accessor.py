import typing
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

from app.base.accessor import BaseAccessor
from app.base.base_model import Base

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

T = typing.TypeVar("T")


class PgAccessor(BaseAccessor):
    def __init__(self, app: "FastAPI"):
        super().__init__(app)
        self.engine: AsyncEngine | None = None
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self):
        self.engine = create_async_engine(
            url=self.app.config.db.url, echo=self.app.config.db.echo
        )
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
        self.session = None

    async def execute_one(
        self, query, model: typing.Type[T] = Base, commit=False
    ) -> typing.Optional[T]:
        async with self.session() as session:
            obj = await session.execute(query)
            if commit:
                await session.commit()
            return obj.scalar_one_or_none()

    async def execute_many(
        self, query, model: typing.Type[T] = Base, commit=False
    ) -> typing.Optional[T]:
        async with self.session() as session:
            obj = await session.execute(query)
            if commit:
                await session.commit()
            return obj.scalars().all()
