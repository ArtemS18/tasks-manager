import logging
import typing
from aiosmtplib import SMTP

from .template import autho_email_template, hello_template, joining_email_template

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI
logger = logging.getLogger(__name__)


class SMTPAccessor:
    def __init__(self, app: "FastAPI"):
        self.app = app
        self.config = app.config.smtp
        self.root_email = self.app.config.smtp.email

    async def get_connect(self) -> SMTP:
        client = SMTP(
            hostname=self.config.host, port=self.config.port, start_tls=self.config.tls
        )
        await client.connect()
        if self.config.remote_connect:
            await client.login(self.config.email, self.config.password)
        return client

    async def send_hello_email(self, user_id: int):
        user = await self.app.store.repo.user.get_user_by_id(user_id)

        msg = hello_template(from_email=self.root_email, to_email=user.login)
        client = await self.get_connect()
        async with client:
            await client.send_message(msg)

    async def send_autho_email(self, user_id: int):
        user = await self.app.store.repo.user.get_user_by_id(user_id)
        password = await self.app.store.redis.get_confirming_password(user_id)

        if password is None:
            return

        msg = autho_email_template(
            from_email=self.root_email, to_email=user.login, password=password
        )
        client = await self.get_connect()
        async with client:
            await client.send_message(msg)
            logger.info(f"Send message to {user.login} from {self.root_email}")

    async def send_joining_in_project_email(
        self, project_id: int, joining_user_id: int, owner_user_id: int
    ):
        joining_user = await self.app.store.repo.user.get_user_by_id(joining_user_id)
        owner_user = await self.app.store.repo.user.get_user_by_id(owner_user_id)
        project = await self.app.store.repo.project.get_project_by_id(project_id)

        msg = joining_email_template(
            from_email=self.root_email,
            to_email=joining_user.login,
            joined_user=joining_user,
            owner_user=owner_user,
            project=project,
        )
        client = await self.get_connect()
        async with client:
            await client.send_message(msg)
            logger.info(f"Send message to {joining_user.login} from {self.root_email}")
