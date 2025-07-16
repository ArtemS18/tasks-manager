from typing import Annotated, List
from fastapi import APIRouter, Depends, Query

from app.lib.fastapi import Request
from app.projects.depends.member import MemberServiceDepend
from app.projects.depends.project import BrokerAccessorDepend, ProjectId
from app.projects.depends.validate import validate_user_in_project, validate_role
from app.projects.models.enums import MemberRole
from app.projects.schemas.filters import BaseFilters, MembersFilters
from app.projects.schemas.members import (
    CreateMemberSchemaRequest,
    Member,
    CreateMemberSchema,
    MemberResponse,
    UpdateMemberDTO,
    UpdateMemberStatus,
)

router = APIRouter(
    prefix="/{project_id}/members",
    tags=["Projects", "Members"],
    dependencies=[Depends(validate_user_in_project)],
)


@router.post("/", dependencies=[Depends(validate_role(MemberRole.admin))])
async def create_member(
    broker_notife: BrokerAccessorDepend,
    member_data: CreateMemberSchemaRequest,
    member_service: MemberServiceDepend,
    project_id: ProjectId,
    current_member: Member = Depends(validate_user_in_project),
) -> Member:
    member = await member_service.create_member(
        CreateMemberSchema(project_id=project_id, **member_data.model_dump())
    )
    await broker_notife.send_join_from_project_email(
        project_id, member.user_id, current_member.user_id
    )
    return member


@router.get("/")
async def get_members(
    project_id: ProjectId,
    member_service: MemberServiceDepend,
    filters: Annotated[MembersFilters, Query()],
) -> List[MemberResponse]:
    members = await member_service.get_members(project_id, filters)
    return members


@router.patch("/{member_id}/status", dependencies=[Depends(validate_role())])
async def update_member_status(
    member_id: int,
    project_id: ProjectId,
    member_service: MemberServiceDepend,
    update_data: UpdateMemberStatus,
) -> Member:
    member = await member_service.update_member(
        project_id,
        member_id,
        update_member_data=UpdateMemberDTO(status=update_data.status),
    )
    return member
