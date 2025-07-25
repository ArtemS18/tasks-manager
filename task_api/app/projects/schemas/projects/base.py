from app.base.base_pydantic import Base


class BaseProject(Base):
    name: str
    owner_id: int
