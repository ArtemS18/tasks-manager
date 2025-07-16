from pydantic import EmailStr, BaseModel
from app.base.base_pydantic import Base
from app.auth.models.enyms import UserStatus


class UserSchemaResponse(Base):
    id: int
    tg_id: int
    name: str
    login: EmailStr


class User(Base):
    id: int
    tg_id: int
    name: str
    login: str
    hashed_password: str
    status: UserStatus


class CreateUserDTO(Base):
    tg_id: int
    name: str
    login: EmailStr
    password: str
