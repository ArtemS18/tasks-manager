from pydantic import BaseModel, Field


class BaseFilters(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, le=200, ge=1)


class TaskFilters(BaseFilters):
    is_author: bool = False
    is_assigned: bool = False
    project_id: int | None = None


class ProjectFilters(BaseFilters):
    is_my: bool | None = None
