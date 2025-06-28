from sqlalchemy import insert, select
from app.api.tasks.schemas import CommentsFilters, TaskFilters

from app.store.bd.models.tasks_models import Task, Comment
from app.entity.dto import CreateTaskDTO
from app.entity.user import User
from app.store.bd.accessor import PgAccessor

class TaskRepository(PgAccessor):
    async def get_tasks(self, filters: TaskFilters):
        query = select(Task)
        if filters.assigned_id is not None:
            query = query.where(Task.assigned_id == filters.assigned_id)
        if filters.author_id is not None:
            query = query.where(Task.author_id == filters.author_id )
        query = query.limit(filters.limit).offset(filters.offset)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalars().all()
        
    async def get_task(self, task_id, filters=None):
        query = select(Task).where(Task.id==task_id)
        async with self.session() as session:
            tasks = await session.execute(query)
            return tasks.scalar_one_or_none()
        
    async def get_comments_from_task(self, task_id: int, filters: CommentsFilters):
        query = select(Comment).where(Comment.task_id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        async with self.session() as session:
            comments = await session.execute(query)
            return comments.scalars().all()
        
    async def get_author_from_task(self, task_id: int, filters: CommentsFilters):
        query = select(User).join(User.id==Task.author_id).where(Task.id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        async with self.session() as session:
            comments = await session.execute(query)
            return comments.scalars()
        
    async def get_assigned_from_task(self, task_id: int, filters: CommentsFilters):
        query = select(User).join(User.id==Task.assigned_id).where(Task.id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        async with self.session() as session:
            comments = await session.execute(query)
            return comments.scalars()
        
    async def create_task(self, create_task: CreateTaskDTO):
        query = insert(Task).values(
            text=create_task.text, 
            status=create_task.status,
            author_id=create_task.author_id,
            assigned_id=create_task.assigned_id
        ).returning(Task)
        async with self.session() as session:
            task = await session.execute(query)
            await session.commit()
            return task.scalar_one_or_none()
        


