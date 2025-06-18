from app.entity.base import Base


class User(Base):
    id: int
    tg_id: int
    name: str
    login: str
    hashed_password: str