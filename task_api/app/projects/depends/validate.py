from logging import getLogger
from typing import List
from fastapi import Depends, Path
from app.auth.depends.validations import validation_access_token
from app.auth.schemas.users import User
from app.projects.depends.project import ProjectServiceDepend
from app.projects.depends.task import TaskServiceDepends
from app.projects.models.enums import MemberRole
from app.projects.schemas.members import Member
from app.web import exception

log = getLogger(__name__)


async def validate_user_in_project(
    project_service: ProjectServiceDepend,
    user: User = Depends(validation_access_token),
    project_id: int = Path(...),
) -> Member:
    log.info(f"Validate user: {user.__str__()} in project")
    member = await project_service.validate_user(project_id, user)
    return member


def validate_role(*args):
    async def wrapper(member: Member = Depends(validate_user_in_project)):
        accept_roles: List[MemberRole] = list(args)
        if MemberRole.owner not in accept_roles:
            accept_roles.append(MemberRole.owner)
        if member.role not in accept_roles:
            raise exception.FORBIDDEN_CANT_USE
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
    if not await task_service.validate_author_task(
        member.project_id, task_id, member.id
    ):
        return False
    return True
