import asyncio
import logging
import sys
from .connect import broker
logger = logging.getLogger(__name__)

@broker.task
async def send_welcome_email_task(user_id: int):
    from app.web.app import app
    logger.info("task is running for %s", user_id)
    await app.store.smtp.send_hello_email(user_id)
    logger.info("task is finished for %s", user_id)


@broker.task
async def send_autho_email_task(user_id: int):
    from app.web.app import app
    logger.info("task is running for %s", user_id)
    await app.store.smtp.send_autho_email(user_id)
    logger.info("task is finished for %s", user_id)

async def setup_with_worker():
    from app.web.app import app
    await app.store.connect_all()

if sys.argv[0].endswith("worker"):
    asyncio.run(setup_with_worker())
