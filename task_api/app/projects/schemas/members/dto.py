from app.base.base_pydantic import Base
from app.projects.models.enums import MemberRole, MemberStatus


class Member(Base):
    id: int
    user_id: int
    project_id: int
    role: MemberRole = MemberRole.member
    status: MemberStatus = MemberStatus.active


class UpdateMemberDTO(Base):
    user_id: int | None = None
    project_id: int | None = None
    role: MemberRole | None = None
    status: MemberStatus | None = None
