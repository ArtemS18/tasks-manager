from typing import List
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    text: str
    status: str
    author_id: int
    assigned_id: int | None = None
    class Config:
        from_attributes = True


class Tasks(BaseModel):
    tasks: List[Task]
