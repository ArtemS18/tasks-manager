from typing import Annotated

from fastapi import Depends
from app.lib.fastapi import Request
from app.projects.services.task import TaskService


def task_service(req: Request):
    return TaskService(req.app.store.repo.task, req.app.store.repo.member)


TaskServiceDepends = Annotated["TaskService", Depends(task_service)]
