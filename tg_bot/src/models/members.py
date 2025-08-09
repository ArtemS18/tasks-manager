from pydantic import EmailStr

from .base import Base


class ShortMemberResponse(Base):
    member_id: int
    user_id: int
    name: str
    login: EmailStr
