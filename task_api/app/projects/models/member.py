from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, ForeignKey, Text, Enum

from app.base.base_model import Base
from app.projects.models.enums import MemberRole, MemberStatus


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
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


class Assign(Base):
    __tablename__ = "assignees"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    member_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=False
    )
