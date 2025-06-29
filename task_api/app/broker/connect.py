from taskiq_aio_pika import AioPikaBroker

from app.web.config import setup_config

def setup_broker() -> AioPikaBroker:
    config = setup_config()
    broker = AioPikaBroker(config.AIOPIKA_URL)
    return broker


broker = setup_broker()

async def connect():
    await broker.startup()

async def disconnect():
    await broker.shutdown()
