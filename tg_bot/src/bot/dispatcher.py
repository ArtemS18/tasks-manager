import typing
from aiogram import Dispatcher
from src.routers.start import router

if typing.TYPE_CHECKING:
    from aiogram import Bot


async def setup_dispatcher(bot: "Bot"):
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
