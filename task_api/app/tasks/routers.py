from typing import Annotated
from fastapi import APIRouter, Query, Depends

from app.auth.depends.validations import validation_access_token
from app.auth.schemas.users import User
from app.tasks.depends import TaskServiceDepends
from app.tasks.schemas.commets import Comments, CreateCommentDTO, Comment
from app.tasks.schemas.filters import CommentsFilters, TaskFilters
from app.tasks.schemas.tasks import CreateTaskDTO, Tasks, Task, UpdateTaskDTO

router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(validation_access_token)]
)


@router.get("/")
async def get_tasks(
    service: TaskServiceDepends,
    filter_query: Annotated[TaskFilters, Query()],
) -> Tasks:
    tasks = await service.get_tasks(filter_query)
    return tasks


@router.get("/{task_id}")
async def get_task(service: TaskServiceDepends, task_id: int) -> Task:
    task = await service.get_task(task_id)
    return task


@router.post("/")
async def create_task(new_task: CreateTaskDTO, service: TaskServiceDepends) -> Task:
    task = await service.create_task(new_task)
    return task


@router.put("/{task_id}")
async def update_task(
    task_id: int, service: TaskServiceDepends, task_data: UpdateTaskDTO
) -> Task:
    task = await service.update_task(task_id, task_data)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, service: TaskServiceDepends) -> Task:
    task = await service.delete_task(task_id)
    return task


@router.get("/{task_id}/comments/")
async def get_comments_from_task(
    task_id: int,
    service: TaskServiceDepends,
    filter_query: Annotated[CommentsFilters, Query()],
) -> Comments:
    comments = await service.get_comments(task_id, filter_query)
    return comments


@router.post("/{task_id}/comments/")
async def create_comments(
    task_id: int,
    service: TaskServiceDepends,
    comment_data: CreateCommentDTO,
    user: User = Depends(validation_access_token),
) -> Comment:
    comment = await service.create_comment(task_id, user, comment_data)
    return comment
