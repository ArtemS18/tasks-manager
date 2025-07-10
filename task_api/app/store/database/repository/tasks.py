from typing import List
from sqlalchemy import delete, insert, select, update
from app.tasks.schemas.commets import CreateCommentDTO
from app.tasks.schemas.filters import CommentsFilters, TaskFilters

from app.tasks.models.tasks import Task, Comment
from app.tasks.schemas.tasks import CreateTaskDTO, UpdateTaskDTO
from app.auth.schemas.users import User
from app.store.database.accessor import PgAccessor


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
        return await self.execute_one(query, Task)

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
        create_values = {k: v for k, v in create_task.model_dump().items()}
        query = insert(Task).values(**create_values).returning(Task)
        return await self.execute_one(query, Task, commit=True)

    async def update_task(self, task_id: int, update_task: UpdateTaskDTO) -> Task:
        update_values = {
            k: v for k, v in update_task.model_dump().items() if v is not None
        }
        query = (
            update(Task)
            .values(**update_values)
            .where(Task.id == task_id)
            .returning(Task)
        )
        res = await self.execute_one(query, Task, commit=True)
        task = await self.get_task(task_id)
        print("update result:", task.__repr__())
        return res

    async def delete_task(self, task_id: int) -> Task:
        query = delete(Task).where(Task.id == task_id).returning(Task)
        return await self.execute_one(query, Task, commit=True)

    async def get_comments_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> List[Comment]:
        query = select(Comment).where(Comment.task_id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[Comment])

    async def create_comment(
        self, task_id: int, comment_data: CreateCommentDTO
    ) -> Comment:
        create_values = {k: v for k, v in comment_data.model_dump().items()}
        query = (
            insert(Comment).values(task_id=task_id, **create_values).returning(Comment)
        )
        return await self.execute_one(query, Comment, commit=True)
