from typing import Any
from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        from_attributes = True


class Response(Base):
    ok: bool
    status: int
    data: Any
