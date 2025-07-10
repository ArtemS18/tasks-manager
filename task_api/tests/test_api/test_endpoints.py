from typing import Annotated
from app.lib.fastapi import FastAPI
import pytest
from httpx import AsyncClient, Cookies
from unittest.mock import AsyncMock


# @pytest.mark.asyncio
# async def test_get_tasks(client: AsyncClient, test_app: FastAPI, auth_client: Cookies):
#     from app.tasks.depends import task_service
#     from app.tasks.schemas.tasks import Tasks, Task

#     fake_data = {
#         "tasks": [
#             {
#                 "id": 1,
#                 "text": "Task1",
#                 "status": "ok",
#                 "author_id": 1,
#                 "assigned_id": None,
#             }
#         ]
#     }

#     fake_task_service = AsyncMock()
#     fake_task_service.get_tasks.return_value = Tasks(
#         tasks=[Task(**i) for i in fake_data["tasks"]]
#     )

#     test_app.dependency_overrides[task_service] = lambda: fake_task_service

#     response = await client.get("/tasks/", cookies=auth_client)

#     assert response.status_code == 200
#     assert response.json() == fake_data


@pytest.mark.asyncio
async def test_create_task_service(test_app: FastAPI, reg_client):
    from app.tasks.controllers.task import TaskService
    from app.tasks.schemas.tasks import Task
    from app.tasks.schemas.tasks import CreateTaskDTO

    data = CreateTaskDTO(
        text="Task1",
        status="ok",
        author_id=reg_client["id"],
        assigned_id=None,
    )

    task_service = TaskService(test_app.store.task)

    assert await task_service.create_task(data) == Task(id=1, **data.model_dump())


@pytest.mark.asyncio
async def test_update_task_service(test_app: FastAPI, reg_client):
    from app.tasks.controllers.task import TaskService
    from app.tasks.schemas.tasks import Task
    from app.tasks.schemas.tasks import UpdateTaskDTO, CreateTaskDTO

    data = CreateTaskDTO(
        text="Task1",
        status="done",
        author_id=reg_client["id"],
        assigned_id=None,
    )

    task_service = TaskService(test_app.store.task)

    task = await task_service.create_task(data)

    up = UpdateTaskDTO(**data.model_dump())
    up.text = "UpdatedTask"

    assert await task_service.update_task(task.id, up) == Task(
        id=task.id, **up.model_dump()
    )
