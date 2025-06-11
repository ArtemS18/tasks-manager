from sqlalchemy import insert, select
from app.bd.session import session_with_commit
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd.models import User
from app.entity.dto import CreateUserDTO

class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_user(self, email: str):
        query = select(User).where(User.login==email)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()
    
    async def create_user(self, new_user:CreateUserDTO):
        query = insert(User).values(
            tg_id=new_user.tg_id,
            name=new_user.name,
            hashed_password=new_user.hashed_password,
            login=new_user.login
        ).returning(User)
        async with session_with_commit() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()

