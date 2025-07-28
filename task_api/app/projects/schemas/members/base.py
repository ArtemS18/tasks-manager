from app.base.base_pydantic import Base
from app.projects.models.enums import MemberRole, MemberStatus


class BeseMember(Base):
    user_id: int
    project_id: int
    role: MemberRole = MemberRole.member
    status: MemberStatus = MemberStatus.active
