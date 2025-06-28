import logging
from .connect import broker
from app.store.broker.email.send_email import send_email


logger = logging.getLogger(__name__)

@broker.task
async def send_welcome_email(user_id: int, ):
    logger.info("task is running for %s", user_id)
    await send_email(user_id)
    logger.info("task is finished for %s", user_id)
