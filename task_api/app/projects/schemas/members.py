from pydantic import EmailStr
from app.base.base_pydantic import Base
from app.projects.models.enums import MemberRole, MemberStatus


class BeseMember(Base):
    user_id: int
    project_id: int
    role: MemberRole = MemberRole.member
    status: MemberStatus = MemberStatus.active


class Member(BeseMember):
    id: int


class MemberResponse(Base):
    member_id: int
    name: str
    login: EmailStr
    tg_id: int
    role: MemberRole
    status: MemberStatus


class CreateMemberSchema(BeseMember):
    pass


class CreateMemberSchemaRequest(Base):
    user_id: int
    role: MemberRole = MemberRole.member
    status: MemberStatus = MemberStatus.active


class UpdateMemberDTO(Base):
    user_id: int | None = None
    project_id: int | None = None
    role: MemberRole | None = None
    status: MemberStatus | None = None


class UpdateMemberStatus(Base):
    status: MemberStatus
