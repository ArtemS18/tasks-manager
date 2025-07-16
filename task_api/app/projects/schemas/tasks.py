from typing import List

from app.base.base_pydantic import Base
from app.lib.shemas import PartialModel
from app.projects.models.enums import TaskStatus


class Task(Base):
    id: int
    text: str
    author_id: int
    project_id: int
    status: TaskStatus = TaskStatus.created


class Tasks(Base):
    tasks: List[Task]


class CreateTaskDTO(Base):
    text: str
    author_id: int
    project_id: int
    assigned_id: List[int] | None = None


class UpdateTaskDTO(Base):
    text: str | None = None
    status: TaskStatus | None = None
    author_id: int | None = None
    assigned_id: List[int] | None = None


class CreateTaskSchema(Base):
    text: str
    assigned_id: List[int] | None = None
