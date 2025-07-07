from typing import Annotated

from fastapi import Cookie, HTTPException, status, Depends

from app.service.auth.login import LoginService
from app.service.auth.jwt import JwtService
from app.service.auth.validation import ValidatioService
from app.service.task import TaskService
from app.service.user import UserService
from app.lib.fastapi import Request


def task_service(req: Request):
    return TaskService(req.app.store.task)


def jwt_service(req: Request) -> JwtService:
    return JwtService(req.app.config)


def login_service(req: Request, auth=Depends(jwt_service)):
    return LoginService(
        repository=req.app.store.user, jwt=auth, redis=req.app.store.redis
    )


def user_service(req: Request):
    return UserService(req.app.store.user)


def validation_service(
    req: Request, jwt=Depends(jwt_service), service=Depends(login_service)
):
    return ValidatioService(service, req.app.store.user, jwt)


async def validation_access_token(
    access_token: Annotated[str | None, Cookie()],
    service: Annotated[ValidatioService, Depends(validation_service)],
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token required. Please provide the 'access_token' cookie.",
        )
    user = await service.validation_user(access_token)
    return user


async def validation_refresh_token(
    refresh_token: Annotated[str | None, Cookie()],
    service: Annotated[ValidatioService, Depends(validation_service)],
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token required. Please provide the 'refresh_token' cookie.",
        )
    user = await service.validation_user(refresh_token)
    await service.validation_refresh_token(user, refresh_token)
    return user


async def validation_confirm_token(
    confirm_token: Annotated[str | None, Cookie()],
    service: Annotated[ValidatioService, Depends(validation_service)],
):
    if confirm_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token required. Please provide the 'confirm_token' cookie.",
        )
    user = await service.validation_user_for_confirm(confirm_token)
    return user


async def validation_internal_token(
    req: Request,
):
    token = req.headers.get("X-Internal-Token")
    if token is None or token != req.app.config.internal.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )

    return token
