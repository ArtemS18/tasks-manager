from typing import Annotated
import typing

from fastapi import Cookie, HTTPException, status, Depends

from app.service.auth.login import LoginService
from app.service.auth.jwt import JwtService
from app.service.task import TaskService
from app.service.user import UserService
from app.lib.fastapi import Request

def task_service(req: Request):
    return TaskService(req.app.store.task)

def jwt_service(req: Request) -> JwtService:
    return JwtService(req.app.config)

def login_service(req: Request, auth=Depends(jwt_service)):
    return LoginService(repository=req.app.store.user, jwt=auth)

def user_service(req: Request):
    return UserService(req.app.store.user)

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


