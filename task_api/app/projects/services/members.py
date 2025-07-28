from app.projects.schemas.filters import BaseFilters, MembersFilters
from app.projects.schemas.members.assigned import (
    AssignedResponseSchema,
    CreateAssignedSchema,
)
from app.projects.schemas.members.dto import Member, UpdateMemberDTO
from app.projects.schemas.members.web import (
    CreateMemberSchema,
    MemberResponse,
    MembersResponse,
)
from app.store.database.repository.members import MemberRepository
from app.store.database.repository.tasks import TaskRepository
from app.web import exception


class MemberService:
    def __init__(self, member_repo: MemberRepository, task_repo: TaskRepository):
        self.member_repo = member_repo
        self.task_repo = task_repo

    async def get_member_full(self, project_id: int, member_id: int) -> Member:
        orm_member = await self.member_repo.get_member_full(project_id, member_id)
        member = MemberResponse.orm_member_validate(orm_member)
        return member

    async def get_member_by_id(self, member_id: int) -> Member:
        orm_member = await self.member_repo.get_member(member_id)
        member = MemberResponse.orm_member_validate(orm_member)
        return member

    async def create_member(self, member_data: CreateMemberSchema) -> MemberResponse:
        orm_member = await self.member_repo.create_member(member_data)
        member = MemberResponse.orm_member_validate(orm_member)
        return member

    async def get_members(
        self, project_id: int, filters: MembersFilters | None = None
    ) -> MembersResponse:
        orm_members = await self.member_repo.get_members_full(project_id, filters)
        members = [MemberResponse.orm_member_validate(obj) for obj in orm_members]
        return MembersResponse(members=members)

    async def update_member(
        self, project_id: int, member_id: int, update_member_data: UpdateMemberDTO
    ) -> MemberResponse:
        orm_member = await self.member_repo.update_member(
            project_id, member_id, update_member_data
        )
        member = MemberResponse.orm_member_validate(orm_member)
        return member

    async def get_assigned(
        self, project_id: int, task_id: int, filters: BaseFilters
    ) -> MembersResponse:
        members_orm = await self.member_repo.get_members_full(
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
        members = [MemberResponse.orm_member_validate(obj) for obj in members_orm]
        return MembersResponse(members=members)

    async def create_assigned(
        self, project_id: int, task_id: int, data: CreateAssignedSchema
    ) -> AssignedResponseSchema:
        await self.task_repo.is_task_exist(project_id, task_id)
        await self.check_member_exists(project_id, data.member_id)
        assigned_orm = await self.member_repo.create_assigned(task_id, data.member_id)
        return AssignedResponseSchema.model_validate(assigned_orm)

    async def delete_member(self, project_id: int, member_id: int) -> MemberResponse:
        orm_member = await self.member_repo.delete_member(project_id, member_id)
        member = MemberResponse.orm_member_validate(orm_member)
        return member

    async def check_member_exists(self, project_id: int, member_id: int) -> None:
        if await self.member_repo.is_exist_member(member_id, project_id) is None:
            raise exception.MEMBER_NOT_FOUND

    async def get_member(self, project_id: int, member_id: int) -> Member:
        orm_member = await self.member_repo.get_member(project_id, member_id)
        member = Member.model_validate(orm_member)
        return member
