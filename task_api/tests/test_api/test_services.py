import asyncio
from typing import Annotated
from app.auth.models.users import User
from app.lib.fastapi import FastAPI
import pytest
from httpx import AsyncClient, Cookies
from unittest.mock import AsyncMock

from app.projects.models.member import Member
from app.projects.models.project import Project
from app.projects.schemas.tasks import Task


@pytest.mark.asyncio
async def test_create_task_service(test_app: FastAPI, create_member: Member):
    from app.projects.services.task import TaskService
    from app.projects.schemas.tasks import Task, CreateTaskDTO

    data = CreateTaskDTO(
        text="Task1",
        author_id=create_member.user_id,
        assigned_id=None,
        project_id=create_member.project_id,
    )

    task_service = TaskService(test_app.store.repo.task, test_app.store.repo.member)

    assert await task_service.create_task(data) == Task(id=1, **data.model_dump())


@pytest.mark.asyncio
async def test_update_task_service(test_app: FastAPI, create_member: Member):
    from app.projects.services.task import TaskService
    from app.projects.schemas.tasks import CreateTaskDTO, UpdateTaskDTO

    data = CreateTaskDTO(
        text="Task1",
        author_id=create_member.user_id,
        assigned_id=None,
        project_id=create_member.project_id,
    )

    task_service = TaskService(test_app.store.repo.task, test_app.store.repo.member)

    old_task = await task_service.create_task(data)

    update_dto = UpdateTaskDTO(text="UpdatedTask")

    new_task = old_task.model_copy()
    new_task.text = "UpdatedTask"

    assert (
        await task_service.update_task(
            create_member.project_id, old_task.id, update_dto
        )
        == new_task
    )


@pytest.mark.asyncio
async def test_member_repo(test_app: FastAPI, create_member: Member, setup_schema):
    from app.projects.schemas.members import Member

    true_member = Member(
        id=create_member.id,
        user_id=create_member.user_id,
        project_id=create_member.project_id,
    )
    pydantic_member = Member.model_validate(create_member)

    assert create_member.status == pydantic_member.status

    assert create_member.id == true_member.id
    assert create_member.user_id == true_member.user_id
    assert create_member.project_id == true_member.project_id


@pytest.mark.asyncio
async def test_get_member_service(
    test_app: FastAPI, create_user: User, create_member: Member
):
    from app.projects.services.members import MemberService
    from app.projects.schemas.members import MemberResponse

    member_data = MemberResponse(
        member_id=create_member.id,
        login=create_user.login,
        name=create_user.name,
        tg_id=create_user.tg_id,
        role=create_member.role,
        status=create_member.status,
    )

    member_service = MemberService(test_app.store.repo.member)
    member_schema = await member_service.get_members(create_member.project_id)

    assert member_schema[0] == member_data


@pytest.mark.asyncio
async def test_get_member_service_with_filters(
    test_app: FastAPI, create_user: User, create_member: Member, create_task: Task
):
    from app.projects.services.members import MemberService
    from app.projects.schemas.members import MemberResponse
    from app.projects.schemas.filters import MembersFilters

    member_data = MemberResponse(
        member_id=create_member.id,
        login=create_user.login,
        name=create_user.name,
        tg_id=create_user.tg_id,
        role=create_member.role,
        status=create_member.status,
    )

    member_service = MemberService(test_app.store.repo.member)

    member_list = await member_service.get_members(
        create_member.project_id, MembersFilters(is_author=True, task_id=create_task.id)
    )
    assert member_list[0] == member_data

    empty_member_list = await member_service.get_members(
        create_member.project_id, MembersFilters(is_author=True, task_id=33993939)
    )
    assert empty_member_list == []
    all_member_list = await member_service.get_members(
        create_member.project_id, MembersFilters()
    )
    assert all_member_list[0] == member_data
