from app.entity.base import Base

class CreateUserDTO(Base):
    tg_id: int
    name: str
    login: str
    password: str

class CreateTaskDTO(Base):
    text: str
    status: str
    author_id: int
    assigned_id: int | None = None

