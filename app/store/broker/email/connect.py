from aiosmtplib import SMTP

from app.web.config import get_current_config

client: SMTP | None = None
async def connect():
    global client
    config = get_current_config()
    client = SMTP(hostname=config.EMAIL_HOST, port=config.EMAIL_PORT)
async def disconnect():
    client.close()