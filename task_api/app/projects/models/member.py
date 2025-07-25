import typing
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, ForeignKey, Text, Enum, UniqueConstraint

from app.auth.models.users import User
from app.base.base_model import Base
from app.lib.db import relationship
from app.projects.models.enums import MemberRole, MemberStatus

if typing.TYPE_CHECKING:
    from app.projects.models.project import Project
    from app.projects.models.tasks import Comment


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False, index=True
    )
    role: Mapped[MemberRole] = mapped_column(
        Enum(MemberRole, name="member_role_enum"),
        default=MemberRole.member,
        server_default=MemberRole.member.value,
    )
    status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus, name="member_status_enum"),
        default=MemberStatus.active,
        server_default=MemberStatus.active.value,
    )
    created_tasks = relationship("Task", back_populates="author")
    assigned_tasks = relationship(
        "Task",
        secondary="assignees",
        back_populates="assigned_members",
    )
    user: Mapped["User"] = relationship("User")
    project: Mapped["Project"] = relationship("Project", back_populates="members")
    comments: Mapped["Comment"] = relationship("Comment", back_populates="author")

    __table_args__ = tuple(
        UniqueConstraint("user_id", "project_id", name="unique_constraint_user_project")
    )


class Assign(Base):
    __tablename__ = "assignees"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    member_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    __table_args__ = tuple(
        UniqueConstraint("member_id", "task_id", name="unique_constraint_task_member")
    )
