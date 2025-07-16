from typing import List
from app.projects.schemas.filters import BaseFilters, MembersFilters
from app.projects.schemas.members import (
    CreateMemberSchema,
    Member,
    MemberResponse,
    UpdateMemberDTO,
)
from app.store.database.repository.members import MemberRepository
from app.web import exception


class MemberService:
    def __init__(self, member_repo: MemberRepository):
        self.member_repo = member_repo

    async def create_member(self, member_data: CreateMemberSchema) -> Member:
        orm_member = await self.member_repo.create_member(member_data)
        member = Member.model_validate(orm_member)
        return member

    async def get_members(
        self, project_id: int, filters: MembersFilters | None = None
    ) -> List[MemberResponse | None]:
        orm_members = await self.member_repo.get_members_with_user_data_by_project_id(
            project_id, filters
        )
        members = [MemberResponse.model_validate(obj) for obj in orm_members]

        return members

    async def update_member(
        self, project_id: int, member_id: int, update_member_data: UpdateMemberDTO
    ) -> Member:
        orm_member = await self.member_repo.update_member(
            project_id, member_id, update_member_data
        )
        member = Member.model_validate(orm_member)

        return member

    async def get_assigned(
        self, project_id: int, task_id: int, filters: BaseFilters
    ) -> List[MemberResponse]:
        members_orm = await self.member_repo.get_members_with_user_data_by_project_id(
            project_id,
            MembersFilters(
                task_id=task_id,
                is_assigned=True,
                limit=filters.limit,
                offset=filters.offset,
            ),
        )
        if members_orm == []:
            raise exception.MEMBER_NOT_FOUND
        members = [MemberResponse.model_validate(obj) for obj in members_orm]
        return members
