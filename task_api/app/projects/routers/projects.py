from typing import Annotated
from fastapi import APIRouter, Body, Depends

from app.auth.depends.validations import validation_access_token

from app.auth.schemas.users import User
from app.projects.depends.project import ProjectServiceDepend
from app.projects.depends.validate import validate_user_in_project
from app.projects.schemas.members.dto import Member
from app.projects.schemas.projects.projects import (
    CreateProjectRequest,
    CreateProjectDTO,
    Project,
)
from app.projects.schemas.projects.web import ProjectResponseSchema

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
async def create_project(
    data: Annotated[CreateProjectRequest, Body()],
    project_service: ProjectServiceDepend,
    current_user: User = Depends(validation_access_token),
) -> Project:
    project = await project_service.create_project(
        CreateProjectDTO(owner_id=current_user.id, **data.model_dump())
    )
    return project


@router.get("/{project_id}", dependencies=[Depends(validate_user_in_project)])
async def get_project(
    project_id: int,
    project_service: ProjectServiceDepend,
) -> ProjectResponseSchema:
    project = await project_service.get_project(project_id)
    return project
