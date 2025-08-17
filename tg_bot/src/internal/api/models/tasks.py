from datetime import datetime
from typing import List

from src.bot.models.enums import TaskPriority, TaskStatus
from .members import ShortMemberResponse
from .base import Base


class BaseTask(Base):
    text: str
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None


class Task(BaseTask):
    id: int
    project_id: int


class Tasks(Base):
    tasks: List[Task]


class CreateTaskSchema(BaseTask):
    assigned_id: List[int] | None = None


class Project(Base):
    id: int
    name: str
    owner_id: int


class Projects(Base):
    projects: list[Project]


class TaskResponseSchema(Base):
    id: int
    author: ShortMemberResponse
    assigns: List[ShortMemberResponse | None] = None
    text: str
    project: Project
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None
    # comments: List[Comment | None] = None
    created_at: datetime | None = None


class TasksResponseSchema(Base):
    tasks: List[TaskResponseSchema]
