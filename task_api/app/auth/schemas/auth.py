from pydantic import BaseModel, EmailStr, Field

from app.auth.schemas.users import User
from app.base.base_pydantic import Base


class AuthoSchema(BaseModel):
    username: EmailStr
    password: str = Field(max_length=63, min_length=8)


class RegisterSchema(Base):
    login: EmailStr
    password: str = Field(max_length=63, min_length=8)
    tg_id: int
    name: str


class ConfirmEmailSchema(BaseModel):
    password: str
    confirm_token: str


class UserCredentials(BaseModel):
    user: User
    data: ConfirmEmailSchema
