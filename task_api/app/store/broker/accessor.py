import typing
from app.base.accessor import BaseAccessor
from taskiq_aio_pika import AioPikaBroker
from app.broker.tasks import setup_tasks
from app.lib.utils import import_obj

if typing.TYPE_CHECKING:
    from app.lib.fastapi import FastAPI


from logging import getLogger

log = getLogger(__name__)


class BrokerAccessor(BaseAccessor):
    BROKER_PATH = "app.broker:broker"
    TASKS_PATH = "app.broker.tasks"

    def __init__(self, app: "FastAPI"):
        super().__init__(app)
        self.broker: AioPikaBroker | None = None
        if self.app.config.env_type == "worker":
            self.broker = import_obj(self.BROKER_PATH)
            log.info(f"Download broker object from {self.BROKER_PATH}")

    async def connect(self):
        if self.broker is None:
            self.broker = AioPikaBroker(self.app.config.rabbit.url)
        if not self.broker.is_worker_process:
            setup_tasks(self.broker)
            await self.broker.startup()

    async def disconnect(self):
        if not self.broker.is_worker_process:
            await self.broker.shutdown()

    def get_task(self, name: str) -> str:
        return f"{self.TASKS_PATH}:{name}"

    async def send_confirm_email(self, user_id: int):
        task_path = self.get_task("send_autho_email_task")
        task = self.broker.get_all_tasks().get(task_path)
        await task.kiq(user_id)
        log.info(f"Task: {task.__repr__()} added in broker")

    async def send_join_from_project_email(
        self,
        project_id: int,
        user_id: int,
        owned_id: int,
    ):
        task_path = self.get_task("send_join_in_project_email_task")
        task = self.broker.get_all_tasks().get(task_path)
        await task.kiq(project_id, user_id, owned_id)
        log.info(f"Task: {task.__repr__()} added in broker")
