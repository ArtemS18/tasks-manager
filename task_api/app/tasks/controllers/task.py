import logging
from app.auth.schemas.users import User
from app.tasks.schemas.filters import CommentsFilters, TaskFilters
from app.tasks.schemas.tasks import CreateTaskDTO, Task, Tasks, UpdateTaskDTO
from app.tasks.schemas.commets import Comment, Comments, CreateCommentDTO
from app.store.database.repository.tasks import TaskRepository

log = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repository):
        self.repository: TaskRepository = repository

    async def get_tasks(self, filters: TaskFilters) -> Tasks:
        tasks_orm = await self.repository.get_tasks(filters)
        return Tasks(tasks=[Task.model_validate(i) for i in tasks_orm])

    async def get_task(self, task_id: int, filtres=None) -> Task:
        task_orm = await self.repository.get_task(task_id, filtres)
        return Task.model_validate(task_orm)

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        task_orm = await self.repository.create_task(create_task)
        return Task.model_validate(task_orm)

    async def update_task(self, task_id: int, update_task: UpdateTaskDTO) -> Task:
        task_orm = await self.repository.update_task(task_id, update_task)
        return Task.model_validate(task_orm)

    async def delete_task(self, task_id: int) -> Task:
        task_orm = await self.repository.delete_task(task_id)
        return Task.model_validate(task_orm)

    async def get_comments(self, task_id: int, filters: CommentsFilters) -> Comments:
        comments_orm = await self.repository.get_comments_from_task(task_id, filters)

        comments = Comments(comments=[Comment.model_validate(i) for i in comments_orm])
        return comments

    async def create_comment(
        self, task_id: int, user: User, comment_data: CreateCommentDTO
    ) -> Comment:
        comment_orm = await self.repository.create_comment(
            task_id, user.id, comment_data
        )
        return Comment.model_validate(comment_orm)
