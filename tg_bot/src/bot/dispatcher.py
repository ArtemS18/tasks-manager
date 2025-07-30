import typing
from aiogram import Dispatcher
from src.bot.bot import bot
from src.routers.start import router
from src.internal.api.accessor import api
import logging

if typing.TYPE_CHECKING:
    from aiogram import Bot


async def on_startup(dispatcher: Dispatcher):
    await api.connect()


async def on_shutdown(dispatcher: Dispatcher):
    await api.disconnect()


def setup_dispatcher(bot: "Bot") -> Dispatcher:
    dp = Dispatcher()

    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


async def polling(dp: Dispatcher, bot: "Bot"):
    logging.basicConfig(level="DEBUG")
    await dp.start_polling(bot)


dp = setup_dispatcher(bot)
