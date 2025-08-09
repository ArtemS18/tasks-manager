from typing import Annotated
from fastapi import APIRouter, Body, Depends, Query

from app.auth.depends.validations import validation_access_token
from app.auth.schemas.users import User, UserSchemaResponse
from app.internal.depends.tasks import InternalServiceDepend
from app.internal.depends.validation import validation_internal_token
from app.internal.schemas.users import UpdateUserSchema
from app.lib.fastapi import Request
from app.projects.schemas.filters import ProjectFilters, TaskCurrentUserFilters
from app.projects.schemas.projects.projects import Projects
from app.projects.schemas.tasks.dto import Tasks
from app.projects.schemas.tasks.web import BaseTasksResponseSchema

router = APIRouter(
    prefix="/users",
    # dependencies=[Depends(validation_internal_token)],
    # include_in_schema=False,
)


@router.get("/", dependencies=[Depends(validation_internal_token)])
async def get_user(req: Request, tg_id: int = Query()) -> UserSchemaResponse:
    res = await req.app.store.repo.user.get_user_by_tg_id(tg_id)
    return UserSchemaResponse.model_validate(res)


@router.get("/{tg_id}/tasks")
async def get_tasks_by_tg_id(
    service: InternalServiceDepend,
    tg_id: int,
    filters: Annotated[TaskCurrentUserFilters, Query()],
) -> Tasks:
    tasks = await service.get_tasks_by_tg_id(tg_id, filters)
    return tasks


@router.get("/{tg_id}/projects")
async def get_projects(
    tg_id: int,
    service: InternalServiceDepend,
    filters: Annotated[ProjectFilters, Query()],
) -> Projects:
    projects = await service.get_projects_by_tg_id(tg_id, filters)
    return projects


@router.patch("/me/tg_id")
async def update_user_tg_id(
    req: Request,
    update: Annotated[UpdateUserSchema, Body()],
    user: User = Depends(validation_access_token),
) -> UserSchemaResponse:
    res = await req.app.store.repo.user.update_user(user.id, tg_id=update.tg_id)
    return UserSchemaResponse.model_validate(res)
