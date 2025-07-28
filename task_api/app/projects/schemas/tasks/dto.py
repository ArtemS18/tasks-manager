from datetime import datetime
from typing import List

from app.base.base_pydantic import Base
from app.projects.models.enums import TaskStatus, TaskPriority
from app.projects.schemas.tasks.base import BaseTask


class Task(BaseTask):
    id: int
    project_id: int


class Tasks(Base):
    tasks: List[Task]


class CreateTaskDTO(BaseTask):
    author_id: int
    project_id: int
    assigned_id: List[int] | None = None


class UpdateTaskDTO(Base):
    text: str | None = None
    status: TaskStatus | None = None
    assigned_id: List[int] | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    deadline: datetime | None = None
