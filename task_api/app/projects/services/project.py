from app.projects.models.enums import MemberRole, MemberStatus
from app.projects.schemas import (
    ProjectResponseSchema,
    CreateProjectDTO,
    Project,
    CreateMemberSchema,
)
from app.store.database.repository.members import MemberRepository
from app.store.database.repository.projects import ProjectRepository
from app.store.database.repository.user import UserRepository
from app.web import exception


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        user_repo: UserRepository,
        member_repo: MemberRepository,
    ):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.member_repo = member_repo

    async def validate_user(self, project_id: int, user_id: int):
        member = await self.member_repo.get_member_by_user_id_and_project_id(
            user_id, project_id
        )
        if member is None or member.status == MemberStatus.blocked:
            raise exception.DENITE

        return member

    async def create_project(self, create_project_data: CreateProjectDTO):
        project = await self.project_repo.create_project(create_project_data)
        await self.member_repo.create_member(
            CreateMemberSchema(
                user_id=create_project_data.owner_id,
                project_id=project.id,
                role=MemberRole.owner,
            )
        )
        return Project.model_validate(project)

    async def get_project(self, project_id: int) -> ProjectResponseSchema:
        project = await self.project_repo.get_project_by_id(project_id)
        if project is None:
            raise exception.PROJECT_NOT_FOUND
        return ProjectResponseSchema.validate_orm(project)
