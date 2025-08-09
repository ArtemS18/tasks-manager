import asyncio
import logging
from aiohttp.web import Application, run_app, post, Request, Response
from src.internal.api.accessor import api
from src.bot.config import config
from src.bot.bot import bot
from aiogram.types import Update
from src.bot.dispatcher import dp


async def handel_webhook(req: Request):
    update_data = await req.json()
    update = Update.model_validate(update_data)
    asyncio.create_task(dp.feed_update(bot, update))
    return Response(status=200)


async def on_startup(app: Application):
    await bot.set_webhook(f"{config.webhook.url}{config.webhook.path}")
    await api.connect()


async def on_shutdown(app: Application):
    await bot.delete_webhook()
    await api.disconnect()


def run_server():
    logger = logging.getLogger(__name__)
    logger.setLevel("WARNING")
    app = Application(logger=None)

    app.add_routes([post(config.webhook.path, handel_webhook)])

    app.on_startup(on_startup)
    app.on_shutdown(on_shutdown)

    run_app(app, host=config.webhook.host, port=config.webhook.port)
