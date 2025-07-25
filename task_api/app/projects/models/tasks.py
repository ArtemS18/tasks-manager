from datetime import datetime
from typing import List
import typing
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Enum, Integer, ForeignKey, Text, DateTime

from app.base.base_model import Base
from app.lib.db import relationship
from app.projects.models.enums import TaskPriority, TaskStatus

if typing.TYPE_CHECKING:
    from app.projects.models.member import Member
    from app.projects.models.project import Project


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
        Integer, ForeignKey("projects.id"), nullable=False, index=True
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, name="task_priority_enum"),
        default=TaskPriority.default,
        server_default=TaskPriority.default.value,
    )
    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=None
    )
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    author: Mapped["Member"] = relationship("Member", back_populates="created_tasks")
    assigned_members: Mapped[List["Member"]] = relationship(
        "Member",
        secondary="assignees",
        back_populates="assigned_tasks",
        passive_deletes=True,
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id"),
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"))
    author: Mapped["Member"] = relationship("Member", back_populates="comments")
    task: Mapped["Task"] = relationship("Task", back_populates="comments")
