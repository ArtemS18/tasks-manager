from typing import Annotated

from fastapi import Cookie, HTTPException, status, Depends

from app.bd.session import get_session
from app.bd.repository.user import UserRepository
from app.service.auth.login import LoginService

from app.service.auth.jwt import JwtService
from app.service.task import TaskService
from app.bd.repository.tasks import TaskRepository
from app.service.user import UserService
from app.web.config import get_config

def task_service(session = Depends(get_session)):
    return TaskService(TaskRepository(session))

def jwt_service():
    config = get_config()
    return JwtService(config)

def login_service(session = Depends(get_session), auth=Depends(jwt_service)):
    return LoginService(UserRepository(session), auth)

def user_service(session = Depends(get_session)):
    return UserService(UserRepository(session))

async def validation_access_token(access_token: Annotated[ str | None, Cookie()], service:Annotated[LoginService, Depends(login_service)]):
    if access_token is None:
        raise  HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Access token required. Please provide the 'access_token' cookie.")
    user = await service.validation_user(access_token)
    return user

async def validation_refresh_token(refresh_token: Annotated[ str | None, Cookie()], service:Annotated[LoginService, Depends(login_service)]):
    if refresh_token is None:
        raise  HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token required. Please provide the 'refresh_token' cookie.")
    user = await service.validation_user(refresh_token)
    await service.validation_refresh_token(user, refresh_token)
    return user


