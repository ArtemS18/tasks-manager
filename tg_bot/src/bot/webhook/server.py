import asyncio
import logging
import typing
from aiohttp.web import Application, run_app, post, Request, Response
from src.internal.api.accessor import api
from src.config import config
from aiogram.types import Update

if typing.TYPE_CHECKING:
    from aiogram import Bot
    from aiogram import Dispatcher


async def handel_webhook(req: Request):
    bot = req.app._state.get("bot")
    dp: "Dispatcher" = req.app._state.get("dp")
    update_data = await req.json()
    update = Update.model_validate(update_data)
    asyncio.create_task(dp.feed_update(bot, update))
    return Response(status=200)


async def on_startup(app: Application):
    bot: "Bot" = app._state.get("bot")
    await bot.set_webhook(f"{config.webhook.url}{config.webhook.path}")
    await api.connect()


async def on_shutdown(app: Application):
    bot: "Bot" = app._state.get("bot")
    await bot.delete_webhook()
    await api.disconnect()


def run_server(dispatcher: "Dispatcher", bot: "Bot"):
    logger = logging.getLogger(__name__)
    logger.setLevel("WARNING")
    app = Application(logger=None)

    app._state["bot"] = bot
    app._state["dp"] = dispatcher

    app.add_routes([post(config.webhook.path, handel_webhook)])

    app.on_startup(on_startup)
    app.on_shutdown(on_shutdown)

    run_app(app, host=config.webhook.host, port=config.webhook.port)
