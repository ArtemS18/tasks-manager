import logging
from app.api.tasks.schemas import CommentsFilters, TaskFilters
from app.entity.dto import CreateTaskDTO
from app.entity.task import Comment, Comments, Task, Tasks
from app.store.bd.repository.tasks import TaskRepository
from app.web.exception import INVALID_DATA

log = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repository):
        self.repository: TaskRepository = repository

    async def get_tasks(self, filters: TaskFilters) -> Tasks:
        tasks = await self.repository.get_tasks(filters)
        return Tasks(tasks=[Task.model_validate(i) for i in tasks])

    async def get_task(self, task_id: int, filtres=None) -> Task:
        task = await self.repository.get_task(task_id, filtres)
        return Task.model_validate(task)

    async def get_comments_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> Comments:
        comments = await self.repository.get_comments_from_task(task_id, filters)
        return Comments(comments=[Comment.model_validate(i) for i in comments])

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        try:
            task = await self.repository.create_task(create_task)
        except Exception as error:
            log.error(error)
            raise INVALID_DATA
        return Task.model_validate(task)
