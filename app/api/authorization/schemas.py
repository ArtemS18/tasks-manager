from pydantic import BaseModel, EmailStr, Field

class AuthorizationRequestSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=63, min_length=8)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str