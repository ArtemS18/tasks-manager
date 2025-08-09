from app.base.base_pydantic import Base
from app.projects.models.enums import TaskStatus


class UpdateTaskStatus(Base):
    status: TaskStatus
