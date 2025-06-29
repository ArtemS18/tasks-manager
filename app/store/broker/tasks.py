import logging
from .connect import broker
from app.store.broker.email.send_email import send_hello_email, send_autho_email

logger = logging.getLogger(__name__)

@broker.task
async def send_welcome_email_task(user_id: int):
    from app.web.app import app
    logger.info("task is running for %s", user_id)
    await send_hello_email(app, user_id)
    logger.info("task is finished for %s", user_id)


@broker.task
async def send_autho_email_task(user_id: int):
    from app.web.app import app
    logger.info("task is running for %s", user_id)
    await send_autho_email(app, user_id)
    logger.info("task is finished for %s", user_id)