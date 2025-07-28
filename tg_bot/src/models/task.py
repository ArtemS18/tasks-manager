from pydantic import BaseModel


class Task(BaseModel):
    id: int
    text: str
    status: str
    author_id: int
    assigned_id: int | None = None
