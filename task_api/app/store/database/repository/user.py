from datetime import datetime
import logging
from sqlalchemy import desc, insert, select, update

from app.projects.models.member import Member
from app.store.database.models import User, RefreshToken
from app.auth.schemas.users import CreateUserDTO
from app.store.database.accessor import PgAccessor
from app.lib.utils import async_time
from app.web import exception

logger = logging.getLogger(__name__)


def check_user_exists(func):
    async def wrapper(
        self: UserRepository, user_id: int | None = None, *args, **kwargs
    ):
        if user_id is None:
            user_id = kwargs.get("user_id")
        if not self.get_user_by_id(user_id):
            raise exception.USER_NOT_FOUND
        res = await func(user_id, *args, **kwargs)
        return res

    return wrapper


class UserRepository(PgAccessor):
    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.login == email)
        return await self.execute_one_or_none(query, User)

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        return await self.execute_one(query, User)

    async def create_user(self, new_user: CreateUserDTO) -> User:
        query = (
            insert(User)
            .values(
                tg_id=new_user.tg_id,
                name=new_user.name,
                hashed_password=new_user.password,
                login=new_user.login,
            )
            .returning(User)
        )
        return await self.execute_one(query, User, commit=True)

    async def create_refresh_token(
        self, token: str, expire: datetime, user_id: int
    ) -> RefreshToken:
        query = (
            insert(RefreshToken)
            .values(token=token, expire_at=expire, user_id=user_id)
            .returning(RefreshToken)
        )
        res = await self.execute_one(query, RefreshToken, commit=True)
        return res

    async def get_refresh_token(self, user_id: int, token: str):
        query = (
            select(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.token == token)
            .limit(1)
        )
        res = await self.execute_one_or_none(query, RefreshToken)
        return res

    async def update_user(self, user_id: int, **kwargs):
        query = update(User).values(**kwargs).where(User.id == user_id).returning(User)
        res = await self.execute_one_or_none(query, User, commit=True)
        if res is None:
            raise exception.USER_NOT_FOUND
        return res

    async def get_user_by_project_id(self, user_id: int, project_id: int):
        query = (
            select(User)
            .join(Member, Member.user_id == User.id)
            .where((User.id == user_id) & (Member.project_id == project_id))
        ).limit(1)
        res = await self.execute_one(query, User)
        return res
