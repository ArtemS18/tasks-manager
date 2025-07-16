from app.base.base_pydantic import Base


class BaseProject(Base):
    name: str
    owner_id: int


class Project(BaseProject):
    id: int


class CreateProjectDTO(BaseProject): ...


class CreateProjectRequest(Base):
    name: str
