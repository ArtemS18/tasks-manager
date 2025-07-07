import logging
from app.entity.dto import CreateUserDTO
from app.entity.user import User
from fastapi.exceptions import HTTPException

from app.web.exception import INVALID_DATA

log = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository):
        self.repository = repository

    async def get_user(self, login):
        user = await self.repository.get_user(login)
        return user

    async def create_user(self, new_user: CreateUserDTO):
        if await self.get_user(new_user.login):
            raise HTTPException(
                status_code=409, detail="Email address already registered."
            )
        try:
            user = await self.repository.create_user(new_user)
        except Exception as error:
            log.error(error)
            raise INVALID_DATA

        return User.model_validate(user)
