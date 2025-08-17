import logging
from aiogram import Bot

from src.config import config

_bot: Bot | None = None


def setup_bot():
    global _bot
    logging.basicConfig(level="DEBUG")
    _bot = Bot(config.token)
    return _bot


bot = setup_bot()
