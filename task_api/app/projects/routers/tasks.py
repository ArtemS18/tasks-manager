from typing import Annotated, List
from fastapi import APIRouter, Path, Query, Depends

from app.projects.depends.member import MemberServiceDepend
from app.projects.depends.project import ProjectId
from app.projects.depends.validate import (
    validate_tasks_edits,
    validate_user_in_project,
    validation_access_token,
)
from app.auth.schemas.users import User
from app.projects.depends.task import TaskServiceDepends
from app.projects.schemas.comments.dto import CreateCommentDTO
from app.projects.schemas.comments.web import (
    CommentResponseSchema,
    CommentsResponseSchema,
)
from app.projects.schemas.filters import BaseFilters, CommentsFilters, TaskFilters
from app.projects.schemas.members.assigned import (
    AssignedResponseSchema,
    CreateAssignedSchema,
)
from app.projects.schemas.members.dto import Member
from app.projects.schemas.members.web import (
    MembersResponse,
)
from app.projects.schemas.tasks.dto import CreateTaskDTO, Task, UpdateTaskDTO
from app.projects.schemas.tasks.web import (
    BaseTaskResponseSchema,
    CreateTaskSchema,
    TaskResponseSchema,
    TasksResponseSchema,
)

router = APIRouter(
    prefix="/{project_id}/tasks",
    tags=["Projects", "Tasks"],
    dependencies=[Depends(validate_user_in_project)],
)


@router.get("/")
async def get_tasks(
    service: TaskServiceDepends,
    filter_query: Annotated[TaskFilters, Query()],
    project_id: ProjectId,
) -> TasksResponseSchema:
    tasks = await service.get_tasks(project_id, filter_query)
    return tasks


@router.get("/{task_id}")
async def get_task(
    service: TaskServiceDepends,
    task_id: int,
    project_id: ProjectId,
) -> TaskResponseSchema:
    task = await service.get_full_task(project_id, task_id)
    return task


@router.post("/")
async def create_task(
    new_task: CreateTaskSchema,
    service: TaskServiceDepends,
    project_id: ProjectId,
    member: Member = Depends(validate_user_in_project),
) -> TaskResponseSchema:
    task = await service.create_task(
        CreateTaskDTO(
            author_id=member.id, project_id=project_id, **new_task.model_dump()
        )
    )
    return task


@router.put("/{task_id}", dependencies=[Depends(validate_tasks_edits)])
async def update_task(
    task_id: int,
    service: TaskServiceDepends,
    task_data: UpdateTaskDTO,
    project_id: ProjectId,
) -> BaseTaskResponseSchema:
    task = await service.update_task(task_id, task_data, project_id)
    return task


@router.delete("/{task_id}", dependencies=[Depends(validate_tasks_edits)])
async def delete_task(
    task_id: int,
    service: TaskServiceDepends,
    project_id: ProjectId,
) -> Task:
    task = await service.delete_task(project_id, task_id)
    return task


@router.get("/{task_id}/comments/")
async def get_comments_from_task(
    project_id: ProjectId,
    task_id: int,
    service: TaskServiceDepends,
    filter_query: Annotated[CommentsFilters, Query()],
) -> CommentsResponseSchema:
    comments = await service.get_comments(project_id, task_id, filter_query)
    return comments


@router.post("/{task_id}/comments/")
async def create_comments(
    task_id: int,
    project_id: ProjectId,
    service: TaskServiceDepends,
    comment_data: CreateCommentDTO,
    member: Member = Depends(validate_user_in_project),
) -> CommentResponseSchema:
    comment = await service.create_comment(project_id, task_id, member, comment_data)
    return comment


@router.get("/{task_id}/assigns/")
async def get_assings(
    task_id: int,
    member_service: MemberServiceDepend,
    filters: Annotated[BaseFilters, Query()],
    project_id: ProjectId,
) -> MembersResponse:
    assigns = await member_service.get_assigned(project_id, task_id, filters)
    return assigns


@router.post("/{task_id}/assigns/")
async def create_assined(
    project_id: ProjectId,
    task_id: int,
    member_service: MemberServiceDepend,
    create_data: CreateAssignedSchema,
) -> AssignedResponseSchema:
    assigns = await member_service.create_assigned(project_id, task_id, create_data)
    return assigns
