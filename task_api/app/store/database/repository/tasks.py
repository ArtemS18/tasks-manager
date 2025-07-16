from typing import List
from sqlalchemy import delete, insert, select, update
from app.projects.schemas.commets import CreateCommentDTO
from app.projects.schemas.filters import BaseFilters, CommentsFilters, TaskFilters

from app.projects.models import Task, Comment, Member, Assign
from app.projects.schemas.tasks import CreateTaskDTO, UpdateTaskDTO
from app.store.database.accessor import PgAccessor, validate_error
from app.web import exception


def check_task_exists(func):
    async def wrapper(self, project_id, task_id, *args, **kwargs):
        if not await self.get_task(project_id, task_id):
            raise exception.TASK_NOT_FOUND
        return await func(self, project_id, task_id, *args, **kwargs)

    return wrapper


class TaskRepository(PgAccessor):
    async def get_tasks(
        self, project_id: int, filters: TaskFilters | None = None
    ) -> List[Task]:
        query = select(Task)
        if filters:
            if filters.assigned_id:
                query = query.join(Assign, Assign.task_id == Task.id).where(
                    Assign.id.in_(filters.assigned_id)
                )
            if filters.author_id:
                query = query.where(Task.author_id == filters.author_id)
        query = (
            query.where(Task.project_id == project_id)
            .limit(filters.limit)
            .offset(filters.offset)
        )
        return await self.execute_many(query, List[Task])

    async def get_task(self, project_id: int, task_id: int, filters=None) -> Task:
        query = select(Task).where(
            (Task.id == task_id) & (Task.project_id == project_id)
        )
        return await self.execute_one(query, Task)

    async def get_author_from_task(self, project_id: int, task_id: int) -> Member:
        query = (
            select(Member)
            .join(Task, Member.id == Task.author_id)
            .where((Task.id == task_id) & (Task.project_id == project_id))
        )
        return await self.execute_one(query, Member)

    @validate_error
    async def create_assigned(self, assigned_id: int, task_id: int):
        if await self.execute_one_or_none(
            select(Assign).where(
                (Assign.member_id == assigned_id) & (Assign.task_id == task_id)
            ),
            Assign,
        ):
            raise exception.BD_ERROR_UNIQUE

        query = (
            insert(Assign)
            .values(task_id=task_id, member_id=assigned_id)
            .returning(Assign)
        )
        return await self.execute_one(query, Assign, commit=True)

    async def get_assigned_from_task(
        self, task_id: int, filters: BaseFilters | None = None
    ) -> List[Member]:
        query = (
            select(Member)
            .join(Assign, Member.id == Assign.member_id)
            .where(Assign.task_id == task_id)
        )
        if filters:
            query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[Member])

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        create_values = {
            k: v for k, v in create_task.model_dump().items() if k != "assigned_id"
        }

        query = insert(Task).values(**create_values).returning(Task)
        new_task = await self.execute_one_or_none(query, Task, commit=True)

        if create_task.assigned_id is not None:
            for member_id in create_task.assigned_id:
                await self.create_assigned(member_id, new_task.id)

        return new_task

    @check_task_exists
    async def update_task(
        self, project_id: int, task_id: int, update_task_data: UpdateTaskDTO
    ) -> Task:
        update_values = {
            k: v
            for k, v in update_task_data.model_dump().items()
            if v is not None and k != "assigned_id"
        }
        if update_values != {}:
            query = (
                update(Task)
                .values(**update_values)
                .where((Task.id == task_id) & (Task.project_id == project_id))
                .returning(Task)
            )
            updated_task = await self.execute_one(query, Task, commit=True)
            return updated_task

        if update_task_data.assigned_id is not None:
            for member_id in update_task_data.assigned_id:
                await self.create_assigned(member_id, task_id)

        return await self.get_task(project_id, task_id)

    @check_task_exists
    async def delete_task(self, project_id: int, task_id: int) -> Task:
        await self.delete_all_assigned(task_id)
        query = (
            delete(Task)
            .where((Task.id == task_id) & (Task.project_id == project_id))
            .returning(Task)
        )
        deleted_task = await self.execute_one(query, Task, commit=True)
        return deleted_task

    async def delete_all_assigned(self, task_id: int):
        assigned_list = await self.get_assigned_from_task(task_id)

        if assigned_list:
            for assing in assigned_list:
                await self.delete_assigned_by_member_id(task_id, assing.id)

    async def delete_assigned_by_member_id(self, task_id: int, member_id: int):
        query = (
            delete(Assign)
            .where((Assign.task_id == task_id) & (Assign.member_id == member_id))
            .returning(Assign)
        )
        return await self.execute_one(query, Assign, commit=True)

    @check_task_exists
    async def get_comments_from_task(
        self, task_id: int, filters: CommentsFilters
    ) -> List[Comment]:
        query = select(Comment).where(Comment.task_id == task_id)
        query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[Comment])

    @check_task_exists
    async def create_comment(
        self, task_id: int, member_id: int, comment_data: CreateCommentDTO
    ) -> Comment:
        create_values = {k: v for k, v in comment_data.model_dump().items()}
        query = (
            insert(Comment)
            .values(task_id=task_id, author_id=member_id, **create_values)
            .returning(Comment)
        )
        return await self.execute_one(query, Comment, commit=True)
