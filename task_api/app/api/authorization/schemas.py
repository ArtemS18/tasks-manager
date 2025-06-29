from typing import Any
from pydantic import EmailStr, Field, BaseModel

class AuthorizationRequestSchema(BaseModel):
    login: str
    password: str = Field(max_length=63, min_length=8)

class OKResponseSchema(BaseModel):
    message: str
    details: Any | None = None

class UserSchemaResponse(BaseModel):
    tg_id: int
    name: str
    login: str
    class Config:
        from_attributes = True

class RegisterUserSchema(AuthorizationRequestSchema):
    tg_id: int
    name: str

class ConfirmEmailSchema(BaseModel):
    password: str