from typing import List
from app.entity.base import Base

class Task(Base):
    id: int
    text: str
    status: str
    author_id: int
    assigned_id: int | None = None


class Tasks(Base):
    tasks: List[Task]


class Comment(Base):
    id: int
    task_id: int
    text: str
    author_id: int


class Comments(Base):
    comments: List[Comment]

