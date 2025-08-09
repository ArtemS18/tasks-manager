from typing import Annotated
from fastapi import APIRouter, Depends, Query

from app.internal.depends.tasks import InternalServiceDepend
from app.internal.depends.validation import validation_internal_token
from app.internal.schemas.tasks import UpdateTaskStatus
from app.projects.depends.task import TaskServiceDepends
from app.projects.schemas.filters import (
    CommentsFilters,
    TaskCurrentUserFilters,
    TaskFilters,
)
from app.projects.schemas import (
    CommentsResponseSchema,
    UpdateTaskDTO,
    TaskResponseSchema,
    BaseTasksResponseSchema,
)
from app.projects.schemas.tasks.web import BaseTaskResponseSchema

router = APIRouter(
    prefix="/tasks",
    # dependencies=[Depends(validation_internal_token)],
    # include_in_schema=False,
)


@router.get("/{task_id}")
async def get_task(
    service: TaskServiceDepends,
    task_id: int,
) -> TaskResponseSchema:
    tasks = await service.get_task_by_id(task_id)
    return tasks


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: int,
    service: TaskServiceDepends,
    update_status: UpdateTaskStatus,
) -> BaseTaskResponseSchema:
    tasks = await service.update_task(
        task_id, UpdateTaskDTO(status=update_status.status)
    )
    return tasks


@router.get("/{task_id}/comments")  # NOTE: FIX ME
async def get_comment_from_task(
    task_id: int,
    service: TaskServiceDepends,
    filter_query: Annotated[CommentsFilters, Query()],
    project_id: int = Query(ge=0),
) -> CommentsResponseSchema:
    comments = await service.get_comments(project_id, task_id, filter_query)
    return comments
