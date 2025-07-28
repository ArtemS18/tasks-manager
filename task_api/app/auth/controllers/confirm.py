import logging

from app.auth.controllers.jwt import JwtService
from app.auth.controllers.password import create_confirm_password
from app.auth.models.enyms import UserStatus
from app.auth.schemas.users import User
from app.store.broker.accessor import BrokerAccessor
from app.store.database.repository.user import UserRepository
from app.store.redis.accessor import RedisAccessor
from app.web.config import BaseConfig
from app.web import exception

log = logging.getLogger(__name__)


class ConfirmEmailService:
    def __init__(
        self,
        config: BaseConfig,
        broker: BrokerAccessor,
        user_repo: UserRepository,
        cache_user: RedisAccessor,
        jwt_service: JwtService,
    ):
        self.config = config
        self.broker_accessor = broker
        self.cache_user = cache_user
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    async def create_and_write_confirming_password(self, user: User) -> str:
        password = create_confirm_password()
        log.info(password)
        await self.cache_user.create_confirming_password(user.id, password)
        return password

    async def send_email_and_get_confirming_token(self, user: User):
        await self.create_and_write_confirming_password(user)
        await self.broker_accessor.send_confirm_email(user.id)
        token = await self.create_confirming_token(user)
        return token

    async def confirm_password_from_email(self, user: User, user_password: str) -> User:
        log.debug(f"Start confirm email {user.login}")
        password = await self.cache_user.get_confirming_password(user.id)
        if password is None:
            raise exception.USER_NOT_FOUND
        if password != user_password:
            raise exception.INVALID_CODE
        user = await self.user_repo.update_user(user.id, status=UserStatus.active.name)
        return user

    async def create_confirming_token(self, user: User) -> str:
        payload = {"sub": user.login, "id": user.id, "token_type": "confirm"}

        token = self.jwt_service.create_token(
            payload, expire=self.config.jwt.confirm_expire
        )
        return token

    async def validation_confirming_token(self, token: str):
        payload = self.jwt_service.verify_token(token)
        email = payload.get("sub")
        if payload.get("token_type") != "confirm":
            raise exception.JWT_BAD_CREDENSIALS
        orm_user = await self.user_repo.get_user_by_email(email)
        if orm_user is None:
            raise exception.USER_NOT_FOUND
        return User.model_validate(orm_user)
