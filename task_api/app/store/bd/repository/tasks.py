from typing import List
from sqlalchemy import insert, select
from app.api.tasks.schemas import CommentsFilters, TaskFilters

from app.store.bd.models.tasks_models import Task, Comment
from app.entity.dto import CreateTaskDTO
from app.entity.user import User
from app.store.bd.accessor import PgAccessor


class TaskRepository(PgAccessor):
    async def get_tasks(self, filters: TaskFilters) -> List[Task]:
        query = select(Task)
        if filters.assigned_id is not None:
            query = query.where(Task.assigned_id == filters.assigned_id)
        if filters.author_id is not None:
            query = query.where(Task.author_id == filters.author_id)
        query = query.limit(filters.limit).offset(filters.offset)
        return await self.execute_many(query, List[Task])

    async def get_task(self, task_id, filters=None) -> Task:
        query = select(Task).where(Task.id == task_id)
        return self.execute_one(query, Task)

    async def get_comments_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> List[Comment]:
        query = select(Comment).where(Comment.task_id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[Comment])

    async def get_author_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> List[User]:
        query = select(User).join(User.id == Task.author_id).where(Task.id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[User])

    async def get_assigned_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> List[User]:
        query = select(User).join(User.id == Task.assigned_id).where(Task.id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[User])

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        query = (
            insert(Task)
            .values(
                text=create_task.text,
                status=create_task.status,
                author_id=create_task.author_id,
                assigned_id=create_task.assigned_id,
            )
            .returning(Task)
        )
        return await self.execute_one(query, Task, commit=True)
