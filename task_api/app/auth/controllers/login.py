from datetime import datetime, timezone
import logging
from fastapi import HTTPException
from app.auth.schemas.auth import AuthoSchema
from app.auth.schemas.token import RefreshToken
from app.store.database.repository.user import UserRepository
from app.auth.schemas.users import CreateUserDTO, User
from app.auth.controllers.jwt import JwtService
from app.auth.controllers.password import (
    verify_password,
    hash_password_async,
)
from app.auth.models.enyms import UserStatus
from app.web.exception import FORBIDDEN, INVALID_DATA, UNAUTHORIZE
from app.lib.utils import async_time

logger = logging.getLogger(__name__)


class LoginService:
    def __init__(self, repository, jwt):
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt

    async def authentication_user_by_email(self, email: str) -> User:
        orm_user = await self.repository.get_user_by_email(email)
        if orm_user is None:
            raise UNAUTHORIZE
        return User.model_validate(orm_user)

    async def authorizition_user(self, form_data: AuthoSchema) -> User:
        user: User = await self.authentication_user_by_email(form_data.username)
        if user.status != UserStatus.active:
            raise FORBIDDEN
        if not verify_password(str(form_data.password), str(user.hashed_password)):
            raise UNAUTHORIZE
        return user

    @async_time
    async def register_user(self, new_user: CreateUserDTO) -> User:
        if await self.repository.get_user_by_email(new_user.login):
            raise HTTPException(
                status_code=409, detail="Email address already registered."
            )
        new_user.password = await hash_password_async(new_user.password)
        try:
            orm_user = await self.repository.create_user(new_user)
        except Exception as error:
            logger.error(error)
            raise INVALID_DATA
        return User.model_validate(orm_user)

    async def create_access_token(self, user: User) -> str:
        payload = {"sub": user.login, "id": user.id, "name": user.name}

        token = self.jwt.create_token(payload)
        return token

    @async_time
    async def create_refresh_token(self, user: User) -> str:
        payload = {"sub": user.login, "id": user.id}
        refresh = self.jwt.create_refresh_token(payload)
        await self.repository.create_refresh_token(
            refresh.token, refresh.expire, user.id
        )
        return refresh.token

    async def validation_refresh_token(self, user: User, refresh_token: str):
        orm_token = await self.repository.get_refresh_token(user.id, refresh_token)
        token = RefreshToken.model_validate(orm_token)
        if token is None:
            raise HTTPException(
                status_code=403, detail="Authorizate error refresh token"
            )
        if token.blocked:
            raise HTTPException(
                status_code=403, detail="Authorizate error refresh token is blocked"
            )
        if token.expire_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expire time out")
        logger.info("New refresh token was created for user %s", user.id)
        return token.token

    async def validation_user(self, token: str | None):
        payload = self.jwt.verify_token(token)
        email = payload.get("sub")
        user = await self.authentication_user_by_email(email)
        return user
