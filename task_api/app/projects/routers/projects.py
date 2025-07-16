from typing import Annotated
from fastapi import APIRouter, Body, Depends

from app.auth.depends.validations import validation_access_token

from app.auth.schemas.users import User
from app.projects.depends.project import ProjectServiceDepend
from app.projects.schemas.projects import (
    CreateProjectRequest,
    CreateProjectDTO,
    Project,
)

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
