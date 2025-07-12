from typing import Annotated

from fastapi import Depends
from app.lib.fastapi import Request
from app.tasks.controllers.task import TaskService


def task_service(req: Request):
    return TaskService(req.app.store.task)


TaskServiceDepends = Annotated["TaskService", Depends(task_service)]
