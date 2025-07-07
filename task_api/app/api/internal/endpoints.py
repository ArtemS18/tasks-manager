from typing import Annotated
import typing
from fastapi import APIRouter, Query, Depends

from app.api.depencies import validation_internal_token, task_service
from app.api.tasks.schemas import (
    CommentsFilters,
    CommentsSchema,
    CreateTaskSchema,
    TaskFilters,
    TaskSchema,
    TasksSchema,
)
from app.entity.dto import CreateTaskDTO
from app.lib.utils import json_response

if typing.TYPE_CHECKING:
    from app.service.task import TaskService

router = APIRouter(
    prefix="/internal",
    tags=["internal"],
    include_in_schema=False,
    dependencies=[Depends(validation_internal_token)],
)


@router.get("/", response_model=TasksSchema)
async def get_tasks(
    service: Annotated["TaskService", Depends(task_service)],
    filter_query: Annotated[TaskFilters, Query()],
):
    tasks = await service.get_tasks(filter_query)
    return json_response(TasksSchema, tasks)


@router.post("/", response_model=TaskSchema)
async def create_task(
    new_task: CreateTaskSchema, service: Annotated["TaskService", Depends(task_service)]
):
    task = await service.create_task(CreateTaskDTO.model_validate(new_task))
    return json_response(TaskSchema, task)


@router.get("/{task_id}/comments", response_model=CommentsSchema)
async def get_comment_from_task(
    task_id: int,
    service: Annotated["TaskService", Depends(task_service)],
    filter_query: Annotated[CommentsFilters, Query()],
):
    comments = await service.get_comments_from_task(task_id, filter_query)
    return json_response(CommentsSchema, comments)
