from datetime import datetime
import logging
from fastapi import HTTPException
from sqlalchemy import desc, insert, select, update

from app.store.bd.models import User, RefreshToken
from app.entity.dto import CreateUserDTO
from app.store.bd.accessor import PgAccessor
from app.lib.utils import async_time

logger = logging.getLogger(__name__)


class UserRepository(PgAccessor):
    @async_time
    async def get_user(self, email: str) -> User:
        query = select(User).where(User.login == email)
        return await self.execute_one(query, User)

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        return await self.execute_one(query, User)

    @async_time
    async def create_user(self, new_user: CreateUserDTO):
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
            .order_by(desc(RefreshToken.created_at))
            .limit(1)
        )
        res = await self.execute_one(query, RefreshToken)
        return res

    async def update_user(self, user_id: int, **kwargs):
        if not await self.get_user_by_id(user_id):
            raise HTTPException(status_code=409, detail="User not found")

        query = update(User).values(**kwargs).where(User.id == user_id).returning(User)
        res = await self.execute_one(query, User, commit=True)
        return res
