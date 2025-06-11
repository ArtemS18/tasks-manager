from typing import Dict

from fastapi import Depends
from app.api.authorization.depencies import login_service
from app.entity.dto import CreateUserDTO
from app.entity.user import User
from fastapi.exceptions import HTTPException

class UserService:
    def __init__(self, repository):
        self.repository = repository


    async def create_user(self, new_user: Dict):
        user = await self.repository.create_user(CreateUserDTO(**new_user))
        return User.model_validate(user)


