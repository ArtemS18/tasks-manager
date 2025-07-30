from pydantic import EmailStr, BaseModel, Field
from app.base.base_pydantic import Base
from app.auth.models.enyms import UserStatus


class UserSchemaResponse(Base):
    id: int
    tg_id: int
    name: str
    login: EmailStr


class User(Base):
    id: int = Field(alias="sub")
    tg_id: int
    name: str | None = None
    login: str
    hashed_password: str | None = None
    status: UserStatus | None = None
    model_config = {"populate_by_name": True}


class CreateUserDTO(Base):
    tg_id: int
    name: str
    login: EmailStr
    password: str


class UserTokenPayload(Base):
    id: int
    tg_id: int
    login: str
