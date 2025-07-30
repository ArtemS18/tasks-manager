from datetime import datetime, timedelta, timezone
import logging
from fastapi import HTTPException
from pydantic import ValidationError
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
from app.web.config import BaseConfig
from app.web import exception
from app.lib.utils import async_time

logger = logging.getLogger(__name__)


class LoginService:
    def __init__(self, config, repository, jwt):
        self.config: BaseConfig = config
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt

        for name, obj in vars(self).items():
            if callable(obj) and not name.startswith("__"):
                setattr(self, name, async_time(obj))

    @staticmethod
    def _base_payload(user: User) -> dict:
        return {"sub": str(user.id), "login": user.login, "tg_id": user.tg_id}

    async def authentication_user_by_email(self, email: str) -> User:
        orm_user = await self.repository.get_user_by_email(email)
        if orm_user is None:
            raise exception.USER_NOT_FOUND
        if orm_user.status != UserStatus.active:
            raise exception.FORBIDDEN
        return User.model_validate(orm_user)

    async def authorizition_user(self, form_data: AuthoSchema) -> User:
        user: User = await self.authentication_user_by_email(form_data.username)
        if not verify_password(str(form_data.password), str(user.hashed_password)):
            raise exception.INVALID_PASSWORD
        return user

    async def register_user(self, new_user: CreateUserDTO) -> User:
        if await self.repository.get_user_by_email(new_user.login):
            raise HTTPException(
                status_code=409, detail="Email address already registered."
            )
        new_user.password = await hash_password_async(new_user.password)
        orm_user = await self.repository.create_user(new_user)
        return User.model_validate(orm_user)

    async def create_access_token(self, user: User) -> str:
        payload = self._base_payload(user)
        payload.update({"token_type": "access"})

        token = self.jwt.create_token(payload)
        return token

    async def create_refresh_token(self, user: User) -> str:
        payload = self._base_payload(user)
        payload.update({"token_type": "refresh"})

        now = datetime.now(timezone.utc)
        expire_at = now + timedelta(minutes=self.config.jwt.refresh_expire)
        refresh_token = self.jwt.create_token(payload, expire_at=expire_at)

        await self.repository.create_refresh_token(refresh_token, expire_at, user.id)
        logger.info("New refresh token was created for user %s", user.id)
        return refresh_token

    async def base_validation_token(
        self, token: str | None, token_type: str = "access"
    ) -> User:
        if token is None:
            raise exception.JWT_MISSING_TOKEN

        payload = self.jwt.verify_token(token)
        if payload.get("token_type") != token_type:
            raise exception.JWT_BAD_CREDENSIALS
        try:
            print(payload)
            user = User.model_validate(payload)
            return user
        except ValidationError:
            raise exception.JWT_BAD_CREDENSIALS

    async def validation_by_id(
        self, token: str | None, token_type: str = "access"
    ) -> int:
        if token is None:
            raise exception.JWT_MISSING_TOKEN

        payload = self.jwt.verify_token(token)
        if payload.get("token_type") != token_type:
            raise exception.JWT_BAD_CREDENSIALS
        id = payload.get("id")
        if id is None:
            raise exception.JWT_BAD_CREDENSIALS
        return id

    async def validation_refresh_token(self, refresh_token: str | None):
        user_data = await self.base_validation_token(
            refresh_token, token_type="refresh"
        )
        user = await self.authentication_user_by_email(user_data.login)
        orm_token = await self.repository.get_refresh_token(user.id, refresh_token)

        if orm_token is None:
            raise exception.REFRESH_TOKEN_NOT_FOUND
        token = RefreshToken.model_validate(orm_token)
        if token.blocked:
            raise exception.FORBIDDEN
        if token.expire_at < datetime.now(timezone.utc):
            raise exception.JWT_TOKEN_EXPIRED
        return user

    async def validation_access_token(self, access_token: str | None):
        user = await self.base_validation_token(access_token, token_type="access")
        return user
