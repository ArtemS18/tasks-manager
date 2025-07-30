import logging
from aiohttp import ClientSession

from src.bot.config import config
from src.models.tasks import TasksResponseSchema

log = logging.getLogger(__name__)


class ApiAccessor:
    INTERNAL_PATH = "internal/"

    def __init__(self, url: str = config.api.url, token: str = config.api.token):
        self.session: ClientSession | None = None
        self.base_url = url
        self.token = token

    async def connect(self):
        self.session = ClientSession(
            base_url=self.base_url + self.INTERNAL_PATH,
            headers={
                "X-Internal-Token": self.token,
                "Autorization:": f"Bearer {self.token}",
            },
        )

    async def disconnect(self):
        if self.session:
            await self.session.close()

    async def fetch_tasks(self, project_id: int) -> TasksResponseSchema:
        async with self.session.get(url=f"tasks/?project_id={project_id}") as response:
            data = await response.json()
            log.info(data)
            return TasksResponseSchema.model_validate(data)


api = ApiAccessor()
