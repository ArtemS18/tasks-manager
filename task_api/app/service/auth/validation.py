from datetime import datetime, timezone
import logging
from fastapi import HTTPException
from app.entity.user import User
from app.service.auth.jwt import JwtService
from app.service.auth.login import LoginService
from app.store.bd.models.users_models import RefreshToken
from app.store.bd.repository.user import UserRepository

logger = logging.getLogger(__name__)


class ValidatioService:
    def __init__(self, login_sevice, repository, jwt):
        self.repository: UserRepository = repository
        self.jwt: JwtService = jwt
        self.service: LoginService = login_sevice

    async def validation_user(self, token: str):
        payload = self.jwt.verify_token(token)
        email = payload.get("sub")
        user = await self.service.authentication_email(email)
        return user

    async def validation_user_for_confirm(self, token: str):
        payload = self.jwt.verify_token(token)
        email = payload.get("sub")
        if payload.get("for_confirm") != 1:
            raise HTTPException(status_code=401, detail="Bad confirm token")
        user = await self.service.authentication_email(email)
        return user

    async def validation_refresh_token(self, user: User, refresh_token: str):
        token: RefreshToken = await self.repository.get_refresh_token(
            user.id, refresh_token
        )
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
