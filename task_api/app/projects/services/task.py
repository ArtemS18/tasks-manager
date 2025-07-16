import logging
from typing import List
from app.auth.schemas.users import User
from app.projects.schemas.filters import (
    BaseFilters,
    CommentsFilters,
    MembersFilters,
    TaskFilters,
)
from app.projects.schemas.members import Member, MemberResponse
from app.projects.schemas.tasks import CreateTaskDTO, Task, Tasks, UpdateTaskDTO
from app.projects.schemas.commets import Comment, Comments, CreateCommentDTO
from app.store.database.repository.members import MemberRepository
from app.store.database.repository.tasks import TaskRepository
from app.web import exception

log = logging.getLogger(__name__)


class TaskService:
    def __init__(self, task_repo: TaskRepository, member_repo: MemberRepository):
        self.task_repo = task_repo
        self.member_repo = member_repo

    async def get_tasks(self, project_id: int, filters: TaskFilters) -> Tasks:
        tasks_orm = await self.task_repo.get_tasks(project_id, filters)
        return Tasks(tasks=[Task.model_validate(i) for i in tasks_orm])

    async def get_task(self, project_id: int, task_id: int, filtres=None) -> Task:
        task_orm = await self.task_repo.get_task(project_id, task_id, filtres)
        return Task.model_validate(task_orm)

    async def validate_author_task(
        self, project_id: int, task_id: int, member_id: int
    ) -> Task:
        task_orm = await self.task_repo.get_task(project_id, task_id)
        if task_orm.author_id != member_id:
            raise exception.FORBIDDEN_CANT_USE
        return Task.model_validate(task_orm)

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        task_orm = await self.task_repo.create_task(create_task)
        return Task.model_validate(task_orm)

    async def update_task(
        self, project_id: int, task_id: int, update_task: UpdateTaskDTO
    ) -> Task:
        print(update_task.model_dump())
        task_orm = await self.task_repo.update_task(project_id, task_id, update_task)
        return Task.model_validate(task_orm)

    async def delete_task(self, project_id: int, task_id: int) -> Task:
        task_orm = await self.task_repo.delete_task(project_id, task_id)
        return Task.model_validate(task_orm)

    async def get_comments(self, task_id: int, filters: CommentsFilters) -> Comments:
        comments_orm = await self.task_repo.get_comments_from_task(task_id, filters)

        comments = Comments(comments=[Comment.model_validate(i) for i in comments_orm])
        return comments

    async def create_comment(
        self, task_id: int, member: Member, comment_data: CreateCommentDTO
    ) -> Comment:
        comment_orm = await self.task_repo.create_comment(
            task_id, member.id, comment_data
        )
        return Comment.model_validate(comment_orm)
