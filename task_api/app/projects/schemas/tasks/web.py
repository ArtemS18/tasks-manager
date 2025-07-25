from datetime import datetime
from typing import List

from app.base.base_pydantic import Base
from app.projects.models.enums import TaskStatus, TaskPriority
from app.projects.schemas.comments.dto import Comment
from app.projects.schemas.members.web import MemberResponse, ShortMemberResponse
from app.projects.models.tasks import Task as TaskORM
from app.projects.schemas.tasks.base import BaseTask


class CreateTaskSchema(BaseTask):
    assigned_id: List[int] | None = None


class TaskResponseSchema(Base):
    id: int
    author: ShortMemberResponse
    assigns: List[ShortMemberResponse | None] = None
    text: str
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

        return cls(
            author=author,
            assigns=assigns,
            comments=comments,
            **orm_task.to_dict(),
        )


class TasksResponseSchema(Base):
    tasks: List[TaskResponseSchema]
