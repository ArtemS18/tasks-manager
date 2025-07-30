from typing import Annotated
from fastapi import APIRouter, Query, Depends

from app.internal.depends import validation_internal_token
from app.projects.depends.task import TaskServiceDepends
from app.projects.schemas.comments.web import CommentsResponseSchema
from app.projects.schemas.filters import CommentsFilters, TaskFilters
from app.projects.schemas.tasks.dto import CreateTaskDTO
from app.projects.schemas.tasks.web import TaskResponseSchema

router = APIRouter(
    prefix="/internal",
    dependencies=[Depends(validation_internal_token)],
    include_in_schema=False,
)


@router.get("/tasks/", response_model=None)
async def get_tasks(
    service: TaskServiceDepends,
    project_id: int = Query(ge=0),
):
    tasks = await service.get_tasks(project_id, None)
    return tasks


@router.post("/")
async def create_task(
    new_task: CreateTaskDTO, service: TaskServiceDepends
) -> TaskResponseSchema:
    task = await service.create_task(new_task)
    return task


@router.get("/{task_id}/comments")
async def get_comment_from_task(
    task_id: int,
    service: TaskServiceDepends,
    filter_query: Annotated[CommentsFilters, Query()],
    project_id: int = Query(ge=0),
) -> CommentsResponseSchema:
    comments = await service.get_comments(project_id, task_id, filter_query)
    return comments
