from logging import getLogger
from typing import Annotated, List
from fastapi import Depends, HTTPException, Path
from app.auth.depends.services import LoginServiceDepends
from app.auth.depends.validations import ValidateAccessToken, validation_access_token
from app.auth.schemas.users import User
from app.projects.depends.member import MemberServiceDepend
from app.projects.depends.project import ProjectServiceDepend
from app.projects.depends.task import TaskServiceDepends
from app.projects.models.enums import MemberRole, RolePermission
from app.projects.schemas.members.dto import Member
from app.web import exception

log = getLogger(__name__)

# PERMISSIONS = {MemberRole.owner: [RolePermission.all_permissions], MemberRole.admin: []}
ROLE_RANKS = {MemberRole.owner: 1, MemberRole.admin: 2, MemberRole.member: 3}


async def validate_user_in_project(
    project_service: ProjectServiceDepend,
    access_token: ValidateAccessToken,
    login: LoginServiceDepends,
    project_id: int = Path(...),
) -> Member:
    user = await login.validation_access_token(access_token)
    member = await project_service.validate_user(project_id, user.id)
    return member


def validate_role(*args):
    async def wrapper(
        member_service: MemberServiceDepend,
        member: Member = Depends(validate_user_in_project),
        member_id: int = Path(...),
    ):
        accept_roles: List[MemberRole] = list(args)
        if MemberRole.owner not in accept_roles:
            accept_roles.append(MemberRole.owner)

        edit_member: Member = await member_service.get_member_by_id(member_id)

        if member.role not in accept_roles:
            raise exception.FORBIDDEN_CANT_USE

        if member_id == member.id:
            raise exception.CANT_EDIT_YOURSELF

        if ROLE_RANKS[edit_member.role] <= ROLE_RANKS[member.role]:
            raise HTTPException(
                status_code=403,
                detail=f"Cant edit settings from member role: {edit_member.role.value}",
            )
        return member

    return wrapper


async def validate_tasks_edits(
    task_service: TaskServiceDepends,
    member: Member = Depends(validate_user_in_project),
    task_id: int = Path(...),
) -> bool:
    log.info(f"Validate task edit: {member.__str__()} in project")
    if member.role in [MemberRole.owner, MemberRole.admin]:
        return True
    if await task_service.validate_author_task(member.project_id, task_id, member.id):
        return True
    raise exception.FORBIDDEN_CANT_USE


def get_member_id(member_id: int = Path(...)):
    return member_id


MemberId = Annotated[int, Depends(get_member_id)]
