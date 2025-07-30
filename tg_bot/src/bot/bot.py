from aiogram import Bot

from src.bot.config import config

_bot: Bot | None = None


def setup_bot():
    global _bot
    _bot = Bot(config.token)
    return _bot


bot = setup_bot()
