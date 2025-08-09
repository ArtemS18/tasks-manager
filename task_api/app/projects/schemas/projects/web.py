from datetime import datetime
from app.base.base_pydantic import Base
from app.projects.models.enums import MemberRole
from app.projects.models.project import Project as ProjectORM
from app.projects.schemas.members.web import ShortMemberResponse


class ProjectResponseSchema(Base):
    id: int
    name: str
    owner: ShortMemberResponse
    members: list[ShortMemberResponse]
    created_at: datetime

    @classmethod
    def validate_orm(cls, project_orm: ProjectORM) -> "ProjectResponseSchema":
        members: list[ShortMemberResponse] = []
        owner: ShortMemberResponse = None
        for obj in project_orm.members:
            member = ShortMemberResponse.orm_member_validate(obj)
            members.append(member)
            if obj.role == MemberRole.owner:
                owner = member
        return cls(
            id=project_orm.id,
            name=project_orm.name,
            owner=owner,
            members=members,
            created_at=project_orm.created_at,
        )


__all__ = ["ProjectResponseSchema"]
