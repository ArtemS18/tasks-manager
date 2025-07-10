from typing import List

from app.base.base_pydantic import Base
from app.lib.shemas import PartialModel


class BaseTask(Base):
    text: str
    status: str
    author_id: int
    assigned_id: int | None = None


class Task(BaseTask):
    id: int


class Tasks(Base):
    tasks: List[Task]


class CreateTaskDTO(BaseTask):
    pass


class UpdateTaskDTO(BaseTask):
    text: str | None = None
    status: str | None = None
    author_id: int | None = None
    assigned_id: int | None = None
