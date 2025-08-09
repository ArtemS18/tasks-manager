from datetime import datetime
from typing import List

from app.base.base_pydantic import Base
from app.projects.models.enums import TaskStatus, TaskPriority
from app.projects.models.tasks import Task as TaskORM
from app.projects.schemas.comments.dto import Comment
from app.projects.schemas.members.web import ShortMemberResponse
from app.projects.schemas.projects import Project
from app.projects.schemas.tasks.base import BaseTask


class CreateTaskSchema(BaseTask):
    assigned_id: List[int] | None = None


class BaseTaskResponseSchema(Base):
    id: int
    author: ShortMemberResponse
    assigns: List[ShortMemberResponse | None] = None
    text: str
    project: Project
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None
    created_at: datetime | None = None

    @classmethod
    def orm_task_validate(
        cls: "BaseTaskResponseSchema", orm_task: TaskORM
    ) -> "BaseTaskResponseSchema":
        author = ShortMemberResponse.orm_member_validate(orm_task.author)
        assigns = [
            ShortMemberResponse.orm_member_validate(obj)
            for obj in orm_task.assigned_members
        ]
        project = Project.model_validate(orm_task.project)
        return cls(
            author=author,
            assigns=assigns,
            project=project,
            **orm_task.to_dict(),
        )


class TaskResponseSchema(Base):
    id: int
    author: ShortMemberResponse
    assigns: List[ShortMemberResponse | None] = None
    text: str
    project: Project
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None
    comments: List[Comment | None] = None
    created_at: datetime | None = None

    @classmethod
    def orm_task_validate(
        cls: "TaskResponseSchema", orm_task: TaskORM
    ) -> "TaskResponseSchema":
        author = ShortMemberResponse.orm_member_validate(orm_task.author)
        assigns = [
            ShortMemberResponse.orm_member_validate(obj)
            for obj in orm_task.assigned_members
        ]
        comments = [Comment.model_validate(obj) for obj in orm_task.comments]
        project = Project.model_validate(orm_task.project)
        return cls(
            author=author,
            assigns=assigns,
            comments=comments,
            project=project,
            **orm_task.to_dict(),
        )


class TasksResponseSchema(Base):
    tasks: List[TaskResponseSchema]


class BaseTasksResponseSchema(Base):
    tasks: List[BaseTaskResponseSchema]


__all__ = [
    "CreateTaskSchema",
    "TaskResponseSchema",
    "TasksResponseSchema",
    "BaseTaskResponseSchema",
    "BaseTasksResponseSchema",
]
