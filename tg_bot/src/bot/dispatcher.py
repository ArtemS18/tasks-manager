import typing
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder

from src.bot.middlewary.di import DIMiddleware
from src.internal.redis.accessor import redis, redis_api
from src.routers.auth import router as auth_router
from src.routers.menu import router as menu_router
from src.internal.api.accessor import api

if typing.TYPE_CHECKING:
    from aiogram import Bot


async def on_startup(dispatcher: Dispatcher):
    await api.connect()
    await redis_api.connect()


async def on_shutdown(dispatcher: Dispatcher):
    await api.disconnect()
    print("on_shutdown")
    await redis.flushdb(asynchronous=True)
    await redis_api.disconnect()


def setup_dispatcher() -> Dispatcher:
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(prefix="bot", with_bot_id=True),
    )
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(DIMiddleware())
    dp.include_routers(auth_router, menu_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def polling(dp: "Dispatcher", bot: "Bot"):
    try:
        await dp.start_polling(bot)
    except Exception:
        pass
