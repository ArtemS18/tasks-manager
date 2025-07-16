import logging
from typing import cast

from taskiq_aio_pika import AioPikaBroker
from fastapi import Request as FastAPIRequest
from app.lib.fastapi import Request
from taskiq import TaskiqDepends

logger = logging.getLogger(__name__)


def setup_tasks(broker: AioPikaBroker):
    logger.info("Adding broker tasks...")

    @broker.task
    async def send_welcome_email_task(
        user_id: int, _req: FastAPIRequest = TaskiqDepends()
    ):
        req = cast(Request, _req)
        await req.app.store.smtp.send_hello_email(user_id)

    @broker.task
    async def send_autho_email_task(
        user_id: int, _req: FastAPIRequest = TaskiqDepends()
    ):
        req = cast(Request, _req)
        await req.app.store.smtp.send_autho_email(user_id)

    @broker.task
    async def send_join_in_project_email_task(
        project_id: int,
        user_id: int,
        owned_id: int,
        _req: FastAPIRequest = TaskiqDepends(),
    ):
        req = cast(Request, _req)
        await req.app.store.smtp.send_joining_in_project_email(
            project_id, user_id, owned_id
        )
