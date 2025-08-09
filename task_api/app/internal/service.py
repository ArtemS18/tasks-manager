from app.projects.schemas.filters import (
    ProjectFilters,
    TaskCurrentUserFilters,
    TaskFilters,
)
from app.projects.schemas import (
    BaseTaskResponseSchema,
    BaseTasksResponseSchema,
    Project,
    Projects,
)
from app.projects.schemas.tasks.dto import Task, Tasks
from app.store.database.repository.projects import ProjectRepository
from app.store.database.repository.tasks import TaskRepository
from app.web import exception


class InternalService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    async def get_tasks_by_tg_id(
        self, tg_id: int, filters: TaskCurrentUserFilters | None = None
    ) -> Tasks:
        tasks_orm = await self.task_repo.get_tasks_by_tg_id(
            tg_id, filters, load_options=False
        )
        if tasks_orm == []:
            raise exception.TASK_NOT_FOUND
        return Tasks(tasks=[Task.model_validate(i) for i in tasks_orm])

    async def get_projects_by_tg_id(
        self, tg_id: int, filters: ProjectFilters | None = None
    ) -> Projects:
        projects_orm = await self.project_repo.get_projects_by_tg_id(tg_id, filters)
        if projects_orm == []:
            raise exception.PROJECT_NOT_FOUND
        return Projects(projects=[Project.model_validate(i) for i in projects_orm])
