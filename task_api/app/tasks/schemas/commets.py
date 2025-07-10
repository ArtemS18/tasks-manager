from typing import List
from app.base.base_pydantic import Base


class Comment(Base):
    id: int
    task_id: int
    text: str
    author_id: int


class Comments(Base):
    comments: List[Comment]


class CreateCommentDTO(Base):
    text: str
    author_id: int
