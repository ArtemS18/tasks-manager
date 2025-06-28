from taskiq_aio_pika import AioPikaBroker

from app.web.config import config

broker = AioPikaBroker(config.AIOPIKA_URL)

async def connect():
    await broker.startup()

async def disconnect():
    await broker.shutdown()