from typing import Annotated
import typing
from fastapi import APIRouter, Request, Depends

from app.api.depencies import task_service
from app.api.tasks.schemas import TasksSchema

if typing.TYPE_CHECKING:
    from app.service.task import TaskService

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/', response_model=UserShema, dependencies=[Depends(validation_token)])
async def create_new_user(service: Annotated["UserService", Depends(task_service)]):
    tasks = await service.get_tasks()
    return tasks



