from typing import Annotated
import typing
from fastapi import APIRouter, Request, Depends

from app.api.depencies import user_service
from app.api.users.schemas import CreateUserSchema, UserSchema

if typing.TYPE_CHECKING:
    from app.service.user import UserService

router = APIRouter(prefix='/users', tags=['Tasks'])

@router.post('/', response_model=UserSchema)
async def create_new_user(new_user:CreateUserSchema, service: Annotated["UserService", Depends(user_service)]):
    tasks = await service.create_user()
    return tasks




