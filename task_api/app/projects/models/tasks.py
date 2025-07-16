from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Enum, Integer, ForeignKey, Text

from app.base.base_model import Base
from app.projects.models.enums import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status_enum"),
        default=TaskStatus.created,
        server_default=TaskStatus.created.value,
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"))
