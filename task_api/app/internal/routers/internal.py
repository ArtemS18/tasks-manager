from typing import Annotated
from fastapi import APIRouter, Query

from app.internal.depends.tasks import InternalServiceDepend
from app.projects.schemas.filters import ProjectFilters
from app.projects.schemas.projects.projects import Projects


router = APIRouter(
    prefix="/internal",
    # include_in_schema=False,
)


@router.get("/projects/{tg_id}")
async def get_projects(
    tg_id: int,
    service: InternalServiceDepend,
    filters: Annotated[ProjectFilters, Query()],
) -> Projects:
    projects = await service.get_projects_by_tg_id(tg_id, filters)
    return projects
