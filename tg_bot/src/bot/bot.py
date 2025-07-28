from aiogram import Bot

from src.bot.config import config
from src.bot.dispatcher import setup_dispatcher


async def setup_bot():
    bot = Bot(config.token)
    await setup_dispatcher(bot)
