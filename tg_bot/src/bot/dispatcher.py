import typing
from aiogram import Dispatcher
from src.bot.bot import bot
from src.routers.auth import router as auth_router
from src.routers.menu import router as menu_router
from src.internal.api.accessor import api

if typing.TYPE_CHECKING:
    from aiogram import Bot


async def on_startup(dispatcher: Dispatcher):
    await api.connect()


async def on_shutdown(dispatcher: Dispatcher):
    await api.disconnect()


def setup_dispatcher(bot: "Bot") -> Dispatcher:
    dp = Dispatcher()

    dp.include_routers(auth_router, menu_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


async def polling(dp: Dispatcher, bot: "Bot"):
    try:
        await dp.start_polling(bot)
    except Exception:
        pass


dp = setup_dispatcher(bot)
