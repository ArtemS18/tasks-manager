from sqlalchemy import insert, select
from app.auth.schemas.users import User
from app.projects.models.project import Project
from app.projects.schemas.projects import CreateProjectDTO
from app.store.database.accessor import PgAccessor


class ProjectRepository(PgAccessor):
    async def create_project(self, create_project: CreateProjectDTO) -> Project:
        query = insert(Project).values(**create_project.model_dump()).returning(Project)
        res = await self.execute_one(query, Project, commit=True)
        return res

    async def get_project_by_id(self, project_id: int) -> Project:
        query = select(Project).where(Project.id == project_id)
        res = await self.execute_one(query, Project)
        return res
