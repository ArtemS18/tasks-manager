from typing import List
from pydantic import BaseModel, Field

from app.projects.models.enums import MemberRole, MemberStatus


class BaseFilters(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, le=200, ge=1)


class TaskFilters(BaseFilters):
    author_id: int | None = Field(default=None, ge=0)
    assigned_id: List[int] | None = None


class CommentsFilters(BaseFilters):
    author_id: int | None = Field(default=None, ge=0)


class MembersFilters(BaseFilters):
    task_id: int | None = Field(default=None, ge=0)
    is_assigned: bool | None = None
    is_author: bool | None = None
    role: MemberRole | None = None
    status: MemberStatus | None = None
