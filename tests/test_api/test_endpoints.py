from fastapi import FastAPI
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.api.depencies import task_service
from app.entity.task import Tasks, Task

@pytest.mark.asyncio
async def test_get_tasks(async_client: AsyncClient, test_app: FastAPI):
    fake_data = {
        "tasks": [
            {
                "id": 1,
                "text": "Task1",
                "status": "ok",
                "author_id": 1,
                "assigned_id": None
            }
        ]
    }

    fake_task_service = AsyncMock()
    fake_task_service.get_tasks.return_value = Tasks(tasks=[Task(**i) for i in fake_data['tasks']])

    test_app.dependency_overrides[task_service] = lambda: fake_task_service

    response = await async_client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == fake_data
