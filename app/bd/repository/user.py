from datetime import datetime, timedelta
import logging
from fastapi import HTTPException, status
from sqlalchemy import desc, insert, select
from app.bd.session import session_with_commit
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import IntegrityError

from app.bd.models import User, RefreshToken
from app.entity.dto import CreateUserDTO
from app.web.exception import INVALID_DATA

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session):
        self.session: async_sessionmaker[AsyncSession] = session

    async def get_user(self, email: str):
        query = select(User).where(User.login==email)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()
    
    async def create_user(self, new_user:CreateUserDTO):
        try:
            query = insert(User).values(
                tg_id=new_user.tg_id,
                name=new_user.name,
                hashed_password=new_user.password,
                login=new_user.login
            ).returning(User)
            async with session_with_commit() as session:
                tasks = await session.execute(query)
                return tasks.scalar_one_or_none()
        except IntegrityError as error:
            logger.error(error)
            raise INVALID_DATA

    async def create_refresh_token(self, token: str, expire: datetime, user_id: int):
            query = insert(RefreshToken).values(token=token, expire_at=expire, user_id=user_id).returning(RefreshToken)
            async with session_with_commit() as session:
                token = await session.execute(query)
                return token.scalar_one_or_none()
            
    async def get_refresh_token(self, user_id: int, token: str):
        query = select(RefreshToken).where(RefreshToken.user_id==user_id, RefreshToken.token==token).order_by(desc(RefreshToken.created_at)).limit(1)
        async with self.session() as session:
            token = await session.execute(query)
            return token.scalar_one_or_none()

