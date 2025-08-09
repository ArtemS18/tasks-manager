from pydantic import EmailStr
from .base import Base
from .enums import UserStatus


class User(Base):
    id: int
    tg_id: int | None
    name: str
    login: EmailStr
