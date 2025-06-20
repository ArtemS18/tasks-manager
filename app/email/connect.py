from aiosmtplib import SMTP

from app.web.config import get_config

_client: SMTP| None = None

def connect():
    global _client
    config = get_config()
    if _client is None:
        _client = SMTP(hostname=config.EMAIL_HOST, port=config.EMAIL_PORT)

def get_client():
    if _client:
        return _client

