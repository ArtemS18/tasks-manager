import logging
from fastapi import HTTPException
from app.store.bd.repository.user import UserRepository
from app.entity.dto import CreateUserDTO
from app.entity.user import User
from app.service.auth.jwt import JwtService
from app.service.auth.password import (
    verify_password,
    hash_password_async,
    create_confirm_password,
)
from app.store.redis.accessor import RedisAccessor
from app.store.bd.models.users_models import UserStatus
from app.web.exception import FORBIDDEN, INVALID_DATA, UNAUTHORIZE
from app.lib.utils import async_time

logger = logging.getLogger(__name__)


class LoginService:
    def __init__(self, repository, jwt, redis):
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt
        self.redis: RedisAccessor = redis

    async def authentication_email(self, email: str) -> User:
        user = await self.repository.get_user(email)
        if user is None:
            raise UNAUTHORIZE
        return User.model_validate(user)

    async def authentication(self, form_data) -> User:
        user: User = await self.authentication_email(form_data.login)
        if user.status != UserStatus.active:
            raise FORBIDDEN
        if not verify_password(str(form_data.password), str(user.hashed_password)):
            raise UNAUTHORIZE
        return user

    async def create_access_token(self, user: User):
        payload = {"sub": user.login, "id": user.id, "name": user.name}

        token = self.jwt.create_access_token(payload)
        return token

    @async_time
    async def create_confirm_token(self, user: User):
        payload = {"sub": user.login, "id": user.id, "for_confirm": 1}
        token = self.jwt.create_confirm_token(payload)
        return token

    async def create_refresh_token(self, user: User):
        payload = {"sub": user.login, "id": user.id}
        refresh = self.jwt.create_refresh_token(payload)
        await self.repository.create_refresh_token(
            refresh.token, refresh.expire, user.id
        )
        return refresh.token

    async def create_confirming_password(self, user: User):
        password = create_confirm_password()
        logger.info(password)
        await self.redis.create_confirming_password(user.id, password)
        return password

    @async_time
    async def register_user(self, new_user: CreateUserDTO):
        if await self.repository.get_user(new_user.login):
            raise HTTPException(
                status_code=409, detail="Email address already registered."
            )
        new_user.password = await hash_password_async(new_user.password)
        try:
            user = await self.repository.create_user(new_user)
        except Exception as error:
            logger.error(error)
            raise INVALID_DATA
        return User.model_validate(user)

    async def confirm_email(self, user: User, user_password: str):
        logger.debug(f"Start confirm email {user.login}")
        password = await self.redis.get_confirming_password(user.id)
        if password is None:
            raise HTTPException(status_code=401, detail="User not found")
        if password != user_password:
            raise HTTPException(status_code=401, detail="Not valid password")
        user = await self.repository.update_user(user.id, status=UserStatus.active.name)
        return user
