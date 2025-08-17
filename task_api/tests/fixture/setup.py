import logging

from app.auth.models.enyms import UserStatus
from app.auth.models.users import User
from app.lib.fastapi import FastAPI
from random import randint
import pytest_asyncio
import pytest

from app.projects.models import Project, Member
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

    id_ = randint(0, 100000)

    create_user = CreateUserDTO(
        tg_id=id_,
        name=f"user{id_}",
        login=f"login{id_}@gmail.com",
        password="123456789",
    )
    user = await test_app.store.repo.user.get_user_by_email(create_user.login)

    if user is None:
        user = await test_app.store.repo.user.create_user(create_user)

    assert user.tg_id == create_user.tg_id
    assert user.name == create_user.name
    return user


@pytest_asyncio.fixture(scope="function")
async def create_project(test_app: FastAPI, create_user: User):
    from app.projects.schemas.projects.projects import CreateProjectDTO

    id_ = randint(0, 100000)

    create_project = CreateProjectDTO(name=f"project{id_}", owner_id=create_user.id)
    project = await test_app.store.repo.project.create_project(create_project)
    return project


@pytest_asyncio.fixture(scope="function")
async def create_member(test_app: FastAPI, create_user: User, create_project: Project):
    from app.projects.schemas.members.web import CreateMemberSchema

    create_member = CreateMemberSchema(
        user_id=create_user.id, project_id=create_project.id
    )
    member = await test_app.store.repo.member.create_member(create_member)
    return member


@pytest_asyncio.fixture(scope="function")
async def create_task(test_app: FastAPI, create_member: Member):
    from app.projects.schemas.tasks.dto import CreateTaskDTO

    create_task = CreateTaskDTO(
        text="Task1",
        author_id=create_member.id,
        project_id=create_member.project_id,
    )
    task = await test_app.store.repo.task.create_task(create_task)
    return task


@pytest_asyncio.fixture(scope="function")
async def project_mock():
    from app.store.database import models

    user = models.User(
        id=1,
        name="User",
        tg_id=10000,
        login="user@gmail.com",
        status=UserStatus.active,
        hashed_password="11111",
    )

    project = models.Project(id=1, name="Project", owner_id=1)
    project.owner = user

    return project


@pytest_asyncio.fixture(scope="function")
async def member_mock(project_mock: Project):
    from app.store.database import models

    user_mock = models.User(
        id=1,
        name="User",
        tg_id=10000,
        login="user@gmail.com",
        status=UserStatus.active,
        hashed_password="11111",
    )

    member = models.Member(
        id=1,
        project_id=project_mock.id,
        user_id=user_mock.id,
        project=project_mock,
        user=user_mock,
    )

    return member


@pytest_asyncio.fixture(scope="function")
async def task_mock(project_mock: Project, member_mock: Member):
    from app.store.database import models

    return models.Task(
        id=1,
        text="Task",
        project_id=project_mock.id,
        author_id=member_mock.id,
        project=project_mock,
        author=member_mock,
    )
