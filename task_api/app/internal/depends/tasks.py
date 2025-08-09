from typing import Annotated
from fastapi import Depends

from app.internal.service import InternalService
from app.lib.fastapi import Request


def get_task_internal_service(req: Request):
    repo = req.app.store.repo
    return InternalService(task_repo=repo.task, project_repo=repo.project)


InternalServiceDepend = Annotated[InternalService, Depends(get_task_internal_service)]
