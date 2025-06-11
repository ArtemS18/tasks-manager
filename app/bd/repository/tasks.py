from sqlalchemy import select
from app.bd.session import session_with_commit
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd.models.tasks_models import Task

class TaskRepository:
    def __init__(self, session):
        self.session = session

    async def get_tasks(self, filters=None):
        query = select(Task)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalars()
    
