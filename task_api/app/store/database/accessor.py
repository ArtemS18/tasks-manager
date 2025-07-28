import typing
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy import Result, exc
from app.base.accessor import BaseAccessor
from app.base.base_model import Base
from app.web import exception
from app.lib.utils import async_time

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

T = typing.TypeVar("T")

log = logging.getLogger(__name__)


def validate_error(func):
    async def wrapper(self, *args, **kwargs):
        try:
            res = await func(self, *args, **kwargs)
            return res
        except exc.IntegrityError as e:
            param = e._message().split("\n")[-1].strip()
            log.error(param)
            raise exception.get_already_exists_http_exeption(param)
        except exc.SQLAlchemyError as e:
            log.error(e)
            raise exception.INVALID_DATA

    return wrapper


class PgAccessor(BaseAccessor):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, obj in cls.__dict__.items():
            if callable(obj) and not name.startswith("__"):
                setattr(cls, name, async_time(obj))

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

    async def _execute(self, query, commit=True) -> Result[T]:
        async with self.session() as session:
            res: Result[T] = await session.execute(query)
            if commit:
                await session.commit()
            return res

    @asynccontextmanager
    async def get_transaction(self) -> typing.AsyncIterator[AsyncSession]:
        async with self.session() as session:
            async with session.begin():
                yield session

    @validate_error
    async def execute_one_or_none(
        self, query, model: typing.Type[T] = Base, commit=False
    ) -> typing.Optional[T]:
        obj = await self._execute(query, commit)
        return obj.scalar_one_or_none()

    @validate_error
    async def execute_one(
        self, query, model: typing.Type[T] = Base, commit=False
    ) -> typing.Optional[T]:
        obj = await self._execute(query, commit)
        return obj.scalar_one()

    @validate_error
    async def execute_many(
        self, query, model: typing.Type[T] = Base, commit=False
    ) -> typing.Optional[T]:
        obj = await self._execute(query, commit)
        return obj.scalars().all()
