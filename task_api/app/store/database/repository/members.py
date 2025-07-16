from datetime import datetime
from logging import getLogger
from typing import List, cast, Tuple
from sqlalchemy import Result, delete, insert, select, update, exc, or_
from app.auth.models.users import User
from app.projects.models.enums import MemberRole, MemberStatus
from app.projects.models.member import Assign
from app.projects.models.tasks import Task
from app.projects.schemas.filters import BaseFilters, MembersFilters
from app.projects.schemas.members import (
    CreateMemberSchema,
    MemberResponse,
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


class MemberRepository(PgAccessor):
    async def get_member(self, member_id: int) -> Member:
        query = select(Member).where(Member.id == member_id)
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
        old_member = await self.get_member_by_user_id_and_project_id(
            user_id=create_member.user_id, project_id=create_member.project_id
        )
        if old_member:
            raise exception.BD_ERROR_UNIQUE
        create_values = create_member.model_dump()
        query = insert(Member).values(**create_values).returning(Member)
        res = await self.execute_one(query, Member, commit=True)
        return res

    async def get_members_by_project(
        self, project_id: int, filters: BaseFilters | None = None
    ) -> List[Member]:
        query = select(Member).where(Member.project_id == project_id)
        if filters:
            query = query_filters.add_base_filters(query, filters)
        res = await self.execute_many(query, List[Member])
        return res

    @check_member_exists
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
        )
        return await self.execute_one(query, Member, commit=True)

    async def get_members_with_user_data_by_project_id(
        self, project_id: int, filters: MembersFilters | None
    ) -> dict:
        query = (
            select(
                Member.id,
                User.name,
                User.login,
                User.tg_id,
                Member.role,
                Member.status,
                Member.created_at,
            )
            .join(User, User.id == Member.user_id)
            .where(Member.project_id == project_id)
        )
        if filters:
            query = query_filters.add_members_filters(query, filters)

        res = await self._execute(query)
        list_items: List[
            Tuple[int, str, str, int, MemberRole, MemberStatus, datetime]
        ] = res.all()

        list_dict = [
            {
                "member_id": member_id,
                "name": name,
                "login": login,
                "tg_id": tg_id,
                "role": role,
                "status": status,
                "created_at": created_at,
            }
            for member_id, name, login, tg_id, role, status, created_at in list_items
        ]
        log.info(list_dict)
        return list_dict
