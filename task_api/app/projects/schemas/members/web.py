from datetime import datetime
import logging
from typing import List, Optional
import typing
import warnings
from pydantic import EmailStr, Field
from app.base.base_pydantic import Base
from app.projects.models.enums import MemberRole, MemberStatus
from app.projects.models.member import Member as MemberORM
from app.projects.schemas.members.base import BeseMember


if typing.TYPE_CHECKING:
    from app.projects.schemas.tasks.dto import Tasks

log = logging.getLogger(__name__)


class ShortMemberResponse(Base):
    member_id: int
    user_id: int
    name: str
    login: EmailStr

    @classmethod
    def orm_member_validate(cls, orm_member: MemberORM) -> "MemberResponse":
        log.info(orm_member.to_dict())
        return cls(
            member_id=orm_member.id,
            name=orm_member.user.name,
            login=orm_member.user.login,
            user_id=orm_member.user.id,
        )


class MemberResponse(Base):
    member_id: int
    user_id: int
    name: str
    login: EmailStr
    tg_id: int
    role: MemberRole
    status: MemberStatus
    created_at: datetime

    @classmethod
    def orm_member_validate(cls, orm_member: MemberORM) -> "MemberResponse":
        return cls(
            member_id=orm_member.id,
            name=orm_member.user.name,
            login=orm_member.user.login,
            tg_id=orm_member.user.tg_id,
            role=orm_member.role,
            status=orm_member.status,
            created_at=orm_member.created_at,
            user_id=orm_member.user.id,
        )


class MemberTasksResponse(MemberResponse):
    created_tasks: List[Optional["Tasks"]] = Field(default_factory=list)
    assigned_tasks: List[Optional["Tasks"]] = Field(default_factory=list)

    @classmethod
    def orm_member_validate(cls, orm_member: MemberORM) -> "MemberTasksResponse":
        member = super().orm_member_validate(orm_member)
        return cls(
            created_tasks=orm_member.created_tasks,
            assigned_tasks=orm_member.assigned_tasks,
            **member.model_dump(),
        )


class MembersResponse(Base):
    members: List[MemberResponse | None]


class CreateMemberSchema(BeseMember):
    pass


class CreateMemberSchemaRequest(Base):
    user_id: int
    role: MemberRole = MemberRole.member
    status: MemberStatus = MemberStatus.active


class UpdateMemberStatus(Base):
    status: MemberStatus


class UpdateMemberRole(Base):
    role: MemberRole


__all__ = [
    "ShortMemberResponse",
    "MemberResponse",
    "MembersResponse",
    "MemberTasksResponse",
    "CreateMemberSchema",
    "CreateMemberSchemaRequest",
    "UpdateMemberStatus",
    "UpdateMemberRole",
]
