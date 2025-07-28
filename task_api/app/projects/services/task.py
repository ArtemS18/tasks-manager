import logging
from app.lib.utils import async_time
from app.projects.schemas.comments.dto import CreateCommentDTO
from app.projects.schemas.filters import (
    CommentsFilters,
    TaskFilters,
)
from app.projects.schemas.members.dto import Member
from app.projects.schemas.tasks.dto import CreateTaskDTO, Task, UpdateTaskDTO
from app.projects.schemas.tasks.web import (
    TasksResponseSchema,
    TaskResponseSchema,
)
from app.projects.schemas.comments.web import (
    CommentResponseSchema,
    CommentsResponseSchema,
)
from app.store.database.repository.members import MemberRepository
from app.store.database.repository.tasks import TaskRepository
from app.web import exception

log = logging.getLogger(__name__)


class TaskService:
    def __init__(self, task_repo: TaskRepository, member_repo: MemberRepository):
        self.task_repo = task_repo
        self.member_repo = member_repo

        for name, obj in TaskService.__dict__.items():
            if callable(obj) and not name.startswith("__"):
                setattr(TaskService, name, async_time(obj))

    async def get_tasks(
        self, project_id: int, filters: TaskFilters
    ) -> TasksResponseSchema:
        tasks_orm = await self.task_repo.get_full_tasks(project_id, filters)
        if tasks_orm == []:
            raise exception.TASK_NOT_FOUND
        return TasksResponseSchema(
            tasks=[TaskResponseSchema.orm_task_validate(i) for i in tasks_orm]
        )

    async def get_task(self, project_id: int, task_id: int, filtres=None) -> Task:
        task_orm = await self.task_repo.get_task(project_id, task_id, filtres)
        return Task.model_validate(task_orm)

    async def validate_author_task(
        self, project_id: int, task_id: int, member_id: int
    ) -> Task:
        task_orm = await self.task_repo.get_task(project_id, task_id)
        if task_orm is None:
            raise exception.TASK_NOT_FOUND
        if task_orm.author_id != member_id:
            raise exception.FORBIDDEN_CANT_USE
        return Task.model_validate(task_orm)

    async def create_task(self, create_task: CreateTaskDTO) -> TaskResponseSchema:
        task_orm = await self.task_repo.create_task(create_task)
        return TaskResponseSchema.orm_task_validate(task_orm)

    async def update_task(
        self, project_id: int, task_id: int, update_task: UpdateTaskDTO
    ) -> Task:
        task_orm = await self.task_repo.update_task(project_id, task_id, update_task)
        return Task.model_validate(task_orm)

    async def delete_task(self, project_id: int, task_id: int) -> Task:
        task_orm = await self.task_repo.delete_task(project_id, task_id)
        return Task.model_validate(task_orm)

    async def get_comments(
        self, project_id: int, task_id: int, filters: CommentsFilters
    ) -> CommentsResponseSchema:
        comments_orm = await self.task_repo.get_comments_from_task(
            project_id, task_id, filters
        )
        if comments_orm == []:
            raise exception.get_not_found_http_exeption("Comments")
        comments = [CommentResponseSchema.orm_comment_validate(i) for i in comments_orm]
        return CommentsResponseSchema(comments=comments)

    async def create_comment(
        self,
        project_id: int,
        task_id: int,
        member: Member,
        comment_data: CreateCommentDTO,
    ) -> CommentResponseSchema:
        await self.check_task_exists(project_id, task_id)
        comment_orm = await self.task_repo.create_comment(
            task_id, member.id, comment_data
        )
        return CommentResponseSchema.orm_comment_validate(comment_orm)

    async def get_full_task(
        self,
        project_id: int,
        task_id: int,
    ) -> TaskResponseSchema:
        orm_task = await self.task_repo.get_task_full(project_id, task_id)
        if orm_task is None:
            raise exception.TASK_NOT_FOUND
        return TaskResponseSchema.orm_task_validate(orm_task)

    async def check_task_exists(self, project_id: int, task_id: int) -> None:
        if await self.task_repo.is_task_exist(project_id, task_id) is None:
            raise exception.TASK_NOT_FOUND
