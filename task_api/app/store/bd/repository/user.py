from datetime import datetime
import logging
from fastapi import HTTPException
from sqlalchemy import desc, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.store.bd.models import User, RefreshToken
from app.entity.dto import CreateUserDTO
from app.store.bd.accessor import PgAccessor
from app.web.exception import INVALID_DATA
from app.web.utils import async_time

logger = logging.getLogger(__name__)

class UserRepository(PgAccessor):
    @async_time
    async def get_user(self, email: str):
        query = select(User).where(User.login==email)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()
        
    async def get_user_by_id(self, user_id:int):
        query = select(User).where(User.id==user_id)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()
    @async_time
    async def create_user(self, new_user:CreateUserDTO):
        try:
            query = insert(User).values(
                tg_id=new_user.tg_id,
                name=new_user.name,
                hashed_password=new_user.password,
                login=new_user.login
            ).returning(User)
            async with self.session() as session:
                tasks = await session.execute(query)
                await session.commit()
                return tasks.scalar_one_or_none()
        except IntegrityError as error:
            logger.error(error)
            raise INVALID_DATA

    async def create_refresh_token(self, token: str, expire: datetime, user_id: int):
            query = insert(RefreshToken).values(token=token, expire_at=expire, user_id=user_id).returning(RefreshToken)
            async with self.session() as session:
                tokens = await session.execute(query)
                await session.commit()
                return tokens.scalar_one_or_none()
            
    async def get_refresh_token(self, user_id: int, token: str):
        query = select(RefreshToken).where(RefreshToken.user_id==user_id, RefreshToken.token==token).order_by(desc(RefreshToken.created_at)).limit(1)
        async with self.session() as session:
            tokens = await session.execute(query)
            return tokens.scalar_one_or_none()
        
    async def update_user(self, user_id: int, **kwargs):
        if not await self.get_user_by_id(user_id):
            raise HTTPException(status_code=409, detail="User not found")
        
        query = update(User).values(**kwargs).where(User.id==user_id).returning(User)
        async with self.session() as session:
            user = await session.execute(query)
            await session.commit()
            return user.scalar_one_or_none()
        
