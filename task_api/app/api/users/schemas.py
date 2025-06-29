from app.entity.user import User
from app.entity.base import Base


class CreateUserSchema(Base):
    tg_id: int
    name: str
    login: str
    password: str

class UserSchema(Base):
    id: int
    tg_id: int
    name: str
    login: str