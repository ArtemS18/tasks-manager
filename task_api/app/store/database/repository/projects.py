from sqlalchemy import insert, select, alias
from sqlalchemy.orm import selectinload
from app.auth.models.users import User
from app.projects.models.enums import MemberRole
from app.projects.models.member import Member
from app.projects.models.project import Project
from app.projects.schemas.projects.projects import CreateProjectDTO
from app.store.database.accessor import PgAccessor


class ProjectRepository(PgAccessor):
    async def create_project(self, create_project: CreateProjectDTO) -> Project:
        query = insert(Project).values(**create_project.model_dump()).returning(Project)
        res = await self.execute_one(query, Project, commit=True)
        return res

    async def get_project_by_id(self, project_id: int) -> Project:
        query = (
            select(Project)
            .where(Project.id == project_id)
            .options(
                selectinload(Project.members).selectinload(Member.user),
                selectinload(Project.owner),
            )
        )
        res = await self.execute_one_or_none(query, Project)
        return res

    async def get_project_by_id_f(self, project_id: int) -> Project:
        query = (
            select(
                Project.id,
                Project.name,
                Project.created_at,
                Member.id,
                Member.user_id,
                Member.status,
                Member.role,
                User.name,
                User.login,
            )
            .join(Member, Member.project_id == Project.id)
            .join(User, User.id == Member.user_id)
            .where(Project.id == project_id)
        )
        res = await self._execute(query)
        list_project = res.all()

        _project_id = list_project[0][0]
        _project_name = list_project[0][1]
        _created_at = list_project[0][2]

        members = []
        owner = {}

        for _, _, _, id, user_id, status, role, name, login in list_project:
            members.append(
                {
                    "member_id": id,
                    "user_id": user_id,
                    "status": status,
                    "role": role,
                    "name": name,
                    "login": login,
                }
            )
            if role == MemberRole.owner.value:
                owner.update(
                    {
                        "member_id": id,
                        "user_id": user_id,
                        "status": status,
                        "role": role,
                        "name": name,
                        "login": login,
                    }
                )

        return {
            "id": _project_id,
            "name": _project_name,
            "created_at": _created_at,
            "members": members,
            "owner": owner,
        }
