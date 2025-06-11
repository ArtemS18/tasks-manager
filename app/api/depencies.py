from typing import Annotated

from fastapi import Cookie, HTTPException, status, Depends

from app.bd.session import get_session
from app.bd.repository.user import UserRepository
from app.service.authentication.login import LoginService

from app.service.task import TaskService
from app.bd.repository.tasks import TaskRepository

def task_service():
    session = get_session()
    return TaskService(TaskRepository(session))

def login_service():
    session = get_session()
    return LoginService(UserRepository(session))

async def validation_token(access_token: Annotated[ str | None, Cookie()], service:Annotated[LoginService, Depends(login_service)]):
    if access_token is None:
        raise  HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Access token required. Please provide the 'access_token' cookie.")
    user = await service.validation_user(access_token)
    return user

