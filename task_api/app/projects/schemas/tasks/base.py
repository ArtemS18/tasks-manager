from app.base.base_pydantic import Base
from datetime import datetime
from app.projects.models.enums import TaskStatus, TaskPriority


class BaseTask(Base):
    text: str
    priority: TaskPriority = TaskPriority.default
    status: TaskStatus = TaskStatus.created
    deadline: datetime | None = None
