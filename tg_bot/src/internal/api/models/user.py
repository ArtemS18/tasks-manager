from pydantic import EmailStr
from .base import Base
from src.bot.models.enums import UserStatus


class User(Base):
    id: int
    tg_id: int | None
    name: str
    login: EmailStr
