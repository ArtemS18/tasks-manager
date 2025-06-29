from typing import List
from pydantic import Field, BaseModel
from app.entity.base import Base

from app.entity.dto import CreateTaskDTO
from app.entity.task import Comment, Comments, Task, Tasks

class BaseFilters(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, le=200, ge=1)

class TaskFilters(BaseFilters):
    author_id: int | None = Field(default=None, ge=0)
    assigned_id: int | None = Field(default=None, ge=0)

class CommentsFilters(BaseFilters):
    pass

class CommentSchema(Comment):
    pass

class CommentsSchema(Comments):
    pass

class TaskSchema(Task):
    pass

class TasksSchema(Tasks):
    pass

class CreateTaskSchema(CreateTaskDTO):
    pass

