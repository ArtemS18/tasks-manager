from typing import Annotated
from fastapi import APIRouter, Query, Depends

from app.internal.depends import validation_internal_token
from app.projects.depends.task import TaskServiceDepends
from app.projects.schemas.comments.dto import Comments
from app.projects.schemas.filters import CommentsFilters, TaskFilters
from app.projects.schemas.tasks.dto import CreateTaskDTO, Tasks, Task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(validation_internal_token)],
    include_in_schema=False,
)


@router.get("/")
async def get_tasks(
    service: TaskServiceDepends,
    filter_query: Annotated[TaskFilters, Query()],
) -> Tasks:
    tasks = await service.get_tasks(filter_query)
    return tasks


@router.post("/")
async def create_task(new_task: CreateTaskDTO, service: TaskServiceDepends) -> Task:
    task = await service.create_task(new_task)
    return task


@router.get("/{task_id}/comments")
async def get_comment_from_task(
    task_id: int,
    service: TaskServiceDepends,
    filter_query: Annotated[CommentsFilters, Query()],
) -> Comments:
    comments = await service.get_comments(task_id, filter_query)
    return comments
