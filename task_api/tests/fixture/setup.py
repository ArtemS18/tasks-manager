import logging
from typing import Any, AsyncGenerator, Generator
from asgi_lifespan import LifespanManager
from app.auth.models.users import User
from app.lib.fastapi import FastAPI
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
import pytest

from app.projects.models.project import Project
from app.projects.schemas.members import Member
from app.web.config import BaseConfig, setup_config

loggeer = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> BaseConfig:
    loggeer.info("Setup config")
    return setup_config()


@pytest_asyncio.fixture(scope="function")
async def test_app(config: BaseConfig) -> FastAPI:
    from app.web.app import setup_app

    loggeer.info("Setup app")
    app = setup_app()
    await app.store.connect_all()
    yield app
    await app.store.disconnect_all()


# @pytest_asyncio.fixture(scope="function")
# async def client(config: BaseConfig, test_app: FastAPI):
#     transport = ASGITransport(app=test_app)
#     async with LifespanManager(test_app):
#         async with AsyncClient(transport=transport, base_url="http://test") as ac:
#             yield ac


@pytest_asyncio.fixture(scope="function")
async def create_user(test_app: FastAPI, setup_schema):
    from app.auth.schemas.users import CreateUserDTO

    create_user = CreateUserDTO(
        tg_id=10000, name="name1", login="login@gmail.com", password="123456789"
    )
    user = await test_app.store.repo.user.get_user_by_email(create_user.login)

    if user is None:
        user = await test_app.store.repo.user.create_user(create_user)

    assert user.tg_id == create_user.tg_id
    assert user.name == create_user.name
    return user


@pytest_asyncio.fixture(scope="function")
async def create_project(test_app: FastAPI, create_user: User):
    from app.projects.schemas.projects import CreateProjectDTO

    create_project = CreateProjectDTO(name="project1", owner_id=create_user.id)
    project = await test_app.store.repo.project.create_project(create_project)
    return project


@pytest_asyncio.fixture(scope="function")
async def create_member(test_app: FastAPI, create_user: User, create_project: Project):
    from app.projects.schemas.members import CreateMemberSchema

    create_member = CreateMemberSchema(
        user_id=create_user.id, project_id=create_project.id
    )
    member = await test_app.store.repo.member.create_member(create_member)
    return member


@pytest_asyncio.fixture(scope="function")
async def create_task(test_app: FastAPI, create_member: Member):
    from app.projects.schemas.tasks import CreateTaskDTO

    create_task = CreateTaskDTO(
        text="Task1",
        author_id=create_member.id,
        project_id=create_member.project_id,
    )
    task = await test_app.store.repo.task.create_task(create_task)
    return task
