from pydantic import BaseModel, Field


class BaseFilters(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, le=200, ge=1)


class TaskFilters(BaseFilters):
    author_id: int | None = Field(default=None, ge=0)
    assigned_id: int | None = Field(default=None, ge=0)


class CommentsFilters(BaseFilters):
    pass
