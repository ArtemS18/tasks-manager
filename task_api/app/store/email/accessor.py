import typing
from aiosmtplib import SMTP
from .template import autho_email_template, hello_template
from app.web.config import get_current_config

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI

class SMTPAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.client: SMTP | None = None

    async def connect(self):
        self.client = SMTP(hostname=self.app.config.EMAIL_HOST, port=self.app.config.EMAIL_PORT)

    async def disconnect(self):
        self.client.close()

    async def send_hello_email(self, user_id: int):
        user = await self.app.store.user.get_user_by_id(user_id)

        msg = hello_template(
            from_email="root@localhost", 
            to_email=user.login
        )

        async with self.client:
            await self.client.send_message(msg)

    async def send_autho_email(self, user_id: int):
        user = await self.app.store.user.get_user_by_id(user_id)
        password = await self.app.store.redis.get_confirming_password(user_id)

        if password is None:
            return

        msg = autho_email_template(
            from_email="root@localhost", 
            to_email=user.login,
            password=password
        )
        print(user,password, msg)
        async with self.client:
            await self.client.send_message(msg)