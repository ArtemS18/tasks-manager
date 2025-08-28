import logging
from aiohttp import ClientSession

from src.internal.api.models.filters import ProjectFilters, TaskFilters
from src.internal.api.models.base import Response
from src.internal.api.models.user import User
from src.config import config
from src.internal.api.models.tasks import (
    Projects,
    TaskResponseSchema,
    Tasks,
    TasksResponseSchema,
)

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

    async def fetch_projects(
        self,
        tg_id: int,
        filters: ProjectFilters,
    ) -> Response:
        query_params = {
            k: str(v) for k, v in filters.model_dump().items() if v is not None
        }
        async with self.session.get(
            url=f"users/{tg_id}/projects", params=query_params
        ) as response:
            data = await response.json()
            if response.status != 200:
                return Response(ok=False, status=response.status, data=data)
            return Response(
                ok=True,
                status=response.status,
                data=Projects.model_validate(data),
            )

    async def fetch_tasks(
        self,
        tg_id: int,
        filters: TaskFilters = TaskFilters(is_assigned=True, is_author=True),
    ) -> Response:
        query_params = {
            k: str(v) for k, v in filters.model_dump().items() if v is not None
        }
        async with self.session.get(
            url=f"users/{tg_id}/tasks", params=query_params
        ) as response:
            data = await response.json()
            if response.status != 200:
                return Response(ok=False, status=response.status, data=data)
            return Response(
                ok=True,
                status=response.status,
                data=Tasks.model_validate(data),
            )

    async def fetch_task(
        self,
        task_id: int,
    ) -> Response:
        async with self.session.get(url=f"tasks/{task_id}") as response:
            data = await response.json()
            if response.status != 200:
                return Response(ok=False, status=response.status, data=data)
            return Response(
                ok=True,
                status=response.status,
                data=TaskResponseSchema.model_validate(data),
            )

    async def check_user(self, tg_id: int) -> Response:
        async with self.session.get(url=f"users/?tg_id={tg_id}") as response:
            data = await response.json()
            if response.status != 200:
                return Response(ok=False, status=response.status, data=data)
            return Response(
                ok=True, status=response.status, data=User.model_validate(data)
            )


api = ApiAccessor()
