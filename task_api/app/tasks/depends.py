from typing import Annotated

from fastapi import Depends, HTTPException, status
from app.auth.depends.services import LoginServiceDepends
from app.auth.depends.validations import ValidateAccessToken
from app.lib.fastapi import Request
from app.tasks.controllers.task import TaskService


def task_service(req: Request):
    return TaskService(req.app.store.task)


async def validation_access_token(
    access_token: ValidateAccessToken,
    service: LoginServiceDepends,
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not found access token",
            headers={"WWW-Autentication": "Bearer"},
        )
    user = await service.validation_user(access_token)
    return user


TaskServiceDepends = Annotated["TaskService", Depends(task_service)]
