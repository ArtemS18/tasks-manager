from typing import List
from sqlalchemy import delete, insert, select, update, exists
from app.projects.models.project import Project
from app.projects.schemas.comments.dto import CreateCommentDTO
from app.projects.schemas.filters import BaseFilters, CommentsFilters, TaskFilters
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.projects.models import Task, Comment, Member, Assign
from app.projects.schemas.tasks.dto import CreateTaskDTO, UpdateTaskDTO
from app.store.database.accessor import PgAccessor, validate_error
from app.store.database.repository import query_filters
from app.web import exception


task_options = (
    selectinload(Task.project),
    selectinload(Task.author).selectinload(Member.user),
    selectinload(Task.comments),
    selectinload(Task.assigned_members).selectinload(Member.user),
)


class TaskRepository(PgAccessor):
    async def is_task_exist(self, project_id: int, task_id: int) -> bool:
        query = select(
            exists().where((Task.id == task_id) & (Task.project_id == project_id))
        )
        res: bool = await self.execute_one(query, commit=False)
        return res

    async def get_full_tasks(
        self, project_id: int, filters: TaskFilters | None = None
    ) -> List[Task]:
        query = select(Task).where(Task.project_id == project_id).options(*task_options)
        if filters:
            if filters.assigned_id:
                query = query.join(Assign, Assign.task_id == Task.id).where(
                    Assign.id.in_(filters.assigned_id)
                )
            if filters.author_id:
                query = query.where(Task.author_id == filters.author_id)
        if filters:
            query = query.limit(filters.limit).offset(filters.offset)
        return await self.execute_many(query, List[Task])

    async def get_task_full(self, project_id: int, task_id: int) -> Task:
        query = (
            select(Task)
            .where((Task.id == task_id) & (Task.project_id == project_id))
            .options(*task_options)
        )
        return await self.execute_one_or_none(query, Task)

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

    async def create_assigned(self, assigned_id: int, task_id: int):
        query = (
            pg_insert(Assign)
            .values(task_id=task_id, member_id=assigned_id)
            .on_conflict_do_nothing(index_elements=["task_id", "member_id"])
            .returning(Assign)
        )
        res = await self.execute_one_or_none(query, Assign, commit=True)
        if res is None:
            raise exception.BD_ERROR_UNIQUE
        return res

    async def get_assignees_from_task(
        self, project_id: int, task_id: int, filters: BaseFilters | None = None
    ) -> List[Member]:
        query = (
            select(Member)
            .join(Assign, Member.id == Assign.member_id)
            .where((Assign.task_id == task_id) & (Member.project_id == project_id))
        )
        if filters:
            query = query.limit(filters.limit).offset(filters.offset)

        return await self.execute_many(query, List[Member])

    async def get_assigned_from_task(
        self, project_id: int, task_id: int, member_id: int
    ) -> Member:
        query = (
            select(Member)
            .join(Assign, Member.id == Assign.member_id)
            .where(
                (Assign.task_id == task_id)
                & (Member.project_id == project_id)
                & (Member.id == member_id)
            )
        )
        return await self.execute_one_or_none(query, Member)

    async def create_assigns_from_task(
        self, project_id: int, task_id: int, assigns: List[int]
    ) -> List[Assign]:
        query = (
            select(Project)
            .where((Project.id == project_id))
            .options(selectinload(Project.members), selectinload(Project.tasks))
        )
        async with self.get_transaction() as session:
            res = await session.execute(query)
            project: Project = res.scalar_one_or_none()
            if (project is None) or (
                task_id not in list(map(lambda x: x.id, project.tasks))
            ):
                raise exception.TASK_NOT_FOUND
            for _id in assigns:
                if _id not in list(map(lambda x: x.id, project.members)):
                    raise exception.get_not_found_http_exeption(f"Member: {_id}")
            vals = [
                {"member_id": member_id, "task_id": task_id} for member_id in assigns
            ]
            insert_query = pg_insert(Assign).values(vals).returning(Assign)
            res = await session.execute(insert_query)
            assigns = res.scalars().all()
            return assigns

    async def create_task(self, create_task: CreateTaskDTO) -> Task:
        create_values = {
            k: v for k, v in create_task.model_dump().items() if k != "assigned_id"
        }

        query = insert(Task).values(**create_values).returning(Task)
        new_task = await self.execute_one_or_none(query, Task, commit=True)

        if create_task.assigned_id is not None:
            await self.create_assigns_from_task(
                create_task.project_id, new_task.id, create_task.assigned_id
            )
        return await self.get_task_full(create_task.project_id, new_task.id)

    async def update_task(
        self, project_id: int, task_id: int, update_task_data: UpdateTaskDTO
    ) -> Task:
        if update_task_data.assigned_id is not None:
            await self.delete_assigned(task_id, update_task_data.assigned_id)
            await self.create_assigns_from_task(task_id, update_task_data.assigned_id)

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
                .options(*task_options)
            )
            updated_task = await self.execute_one_or_none(query, Task, commit=True)
            if updated_task is None:
                raise exception.TASK_NOT_FOUND
            return updated_task

        return await self.get_task(project_id, task_id)

    async def delete_task(
        self,
        project_id: int,
        task_id: int,
    ) -> Task:
        query = (
            delete(Task)
            .where((Task.id == task_id) & (Task.project_id == project_id))
            .returning(Task)
        )
        deleted_task = await self.execute_one_or_none(query, Task)
        if deleted_task is None:
            raise exception.TASK_NOT_FOUND
        return deleted_task

    async def delete_assigned(
        self, task_id: int, member_id: int | None, commit: bool = True
    ):
        query = delete(Assign)
        if member_id is None:
            query = query.where((Assign.task_id == task_id))
        else:
            query = query.where(
                (Assign.task_id == task_id) & (Assign.member_id == member_id)
            )
        query = query.returning(Assign)
        return await self.execute_one(query, Assign, commit=commit)

    async def get_comments_from_task(
        self, project_id: int, task_id: int, filters: CommentsFilters | None = None
    ) -> List[Comment]:
        query = (
            select(Comment)
            .join(Task, Task.id == Comment.task_id)
            .where((Comment.task_id == task_id) & (Task.project_id == project_id))
            .options(
                selectinload(Comment.author).selectinload(Member.user),
                selectinload(Comment.task),
            )
        )
        if filters:
            query = query_filters.add_comment_filters(query, filters)
        return await self.execute_many(query, List[Comment])

    async def get_comment_from_task(
        self, task_id: int, comment_id: int, project_id: int | None = None
    ) -> Comment:
        query = (
            select(Comment)
            .join(Task, Task.id == Comment.task_id)
            .where((Comment.task_id == task_id) & (Comment.id == comment_id))
        )
        if project_id is not None:
            query = query.where(Task.project_id == project_id)
        query = query.options(
            selectinload(Comment.author).selectinload(Member.user),
            selectinload(Comment.task),
        )
        return await self.execute_one_or_none(query, Comment)

    async def create_comment(
        self,
        task_id: int,
        member_id: int,
        comment_data: CreateCommentDTO,
    ) -> Comment:
        create_values = {k: v for k, v in comment_data.model_dump().items()}
        insert_query = (
            insert(Comment)
            .values(task_id=task_id, author_id=member_id, **create_values)
            .returning(Comment.id)
        )
        comment_id = await self.execute_one_or_none(insert_query, commit=True)
        if comment_id is None:
            raise exception.TASK_NOT_FOUND

        comment = await self.get_comment_from_task(task_id, comment_id)
        return comment
