from datetime import datetime
from typing import List

from .enums import TaskPriority, TaskStatus
from .members import ShortMemberResponse
from .base import Base


class BaseTask(Base):
    text: str
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None


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
    # comments: List[Comment | None] = None
    created_at: datetime | None = None


class TasksResponseSchema(Base):
    tasks: List[TaskResponseSchema]
