from app.entity.dto import CreateUserDTO
from app.entity.user import User
from fastapi.exceptions import HTTPException

class UserService:
    def __init__(self, repository):
        self.repository = repository

    async def get_user(self, login):
        user = await self.repository.get_user(login)
        return user

    async def create_user(self, new_user: CreateUserDTO):
        if await self.get_user(new_user.login):
            raise HTTPException(status_code=409, detail="Email address already registered.")
        user = await self.repository.create_user(new_user)
        return User.model_validate(user)


