from logging import getLogger
from typing import List
from sqlalchemy import delete, exists, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.projects.models.member import Assign
from app.projects.schemas.filters import BaseFilters, MembersFilters
from app.projects.schemas import (
    CreateMemberSchema,
    UpdateMemberDTO,
)

from app.projects.models import Member
from app.store.database.accessor import PgAccessor
from app.store.database.repository import query_filters
from app.web import exception

log = getLogger(__name__)


def check_member_exists(func):
    async def wrapper(self, member_id, *args, **kwargs):
        if not await self.get_member(member_id):
            raise exception.TASK_NOT_FOUND
        return await func(self, member_id, *args, **kwargs)

    return wrapper


member_options = (selectinload(Member.user), selectinload(Member.project))


class MemberRepository(PgAccessor):
    async def is_exist_member(self, member_id: int, project_id: int) -> bool:
        query = select(
            exists()
            .where(Member.id == member_id)
            .where(Member.project_id == project_id)
        )
        res: bool = await self.execute_one(query)
        return res

    async def get_member(self, member_id: int) -> Member:
        query = select(Member).where(Member.id == member_id).options(*member_options)
        res = await self.execute_one_or_none(query, Member)
        return res

    async def get_member_by_user_id_and_project_id(
        self, user_id: int, project_id: int
    ) -> Member:
        query = select(Member).where(
            (Member.user_id == user_id) & (Member.project_id == project_id)
        )
        res = await self.execute_one_or_none(query, Member)
        return res

    async def create_member(self, create_member: CreateMemberSchema) -> Member:
        create_values = create_member.model_dump()
        query = (
            pg_insert(Member)
            .values(**create_values)
            .on_conflict_do_nothing(index_elements=["project_id", "user_id"])
            .returning(Member)
            .options(*member_options)
        )
        res = await self.execute_one_or_none(query, Member, commit=True)
        if res is None:
            raise exception.BD_ERROR_UNIQUE
        return res

    async def get_members_by_project(
        self, project_id: int, filters: BaseFilters | None = None
    ) -> List[Member]:
        query = select(Member).where(Member.project_id == project_id)
        if filters:
            query = query_filters.add_base_filters(query, filters)
        res = await self.execute_many(query, List[Member])
        return res

    async def get_member_by_project(self, project_id: int, member_id: int) -> Member:
        query = select(Member).where(
            (Member.project_id == project_id) & (Member.id == member_id)
        )
        res = await self.execute_one_or_none(query, Member)
        if res is None:
            raise exception.MEMBER_NOT_FOUND
        return res

    async def update_member(
        self, poject_id: int, member_id: int, member_data: UpdateMemberDTO
    ) -> Member:
        update_values = {
            k: v for k, v in member_data.model_dump().items() if v is not None
        }
        query = (
            update(Member)
            .values(**update_values)
            .where((Member.project_id == poject_id) & (Member.id == member_id))
            .returning(Member)
            .options(*member_options)
        )
        res = await self.execute_one_or_none(query, Member, commit=True)
        if res is None:
            raise exception.MEMBER_NOT_FOUND
        return res

    async def get_members_full(
        self, project_id: int, filters: MembersFilters | None
    ) -> Member:
        query = (
            select(Member)
            .where(Member.project_id == project_id)
            .options(*member_options)
        )
        if filters:
            query = query_filters.add_members_filters(query, filters)

        members = await self.execute_many(query, Member)
        if members == []:
            raise exception.MEMBER_NOT_FOUND
        return members

    async def get_member_full(self, project_id: int, member_id: int) -> Member:
        query = (
            select(Member)
            .where((Member.project_id == project_id) & (Member.id == member_id))
            .options(*member_options)
        )
        member = await self.execute_one_or_none(query, Member)
        if member is None:
            raise exception.MEMBER_NOT_FOUND
        return member

    async def delete_member(self, project_id: int, member_id: int) -> Member:
        query = (
            delete(Member)
            .where((Member.project_id == project_id) & (Member.id == member_id))
            .returning(Member)
        )
        member = await self.execute_one_or_none(query, Member)
        if member is None:
            raise exception.MEMBER_NOT_FOUND
        return member

    async def create_assigned(self, task_id: int, member_id: int):
        query = (
            pg_insert(Assign)
            .values(task_id=task_id, member_id=member_id)
            .on_conflict_do_nothing(index_elements=["task_id", "member_id"])
            .returning(Assign)
        )
        res = await self.execute_one_or_none(query, commit=True)

        if res is None:
            raise exception.BD_ERROR_UNIQUE
        return res
