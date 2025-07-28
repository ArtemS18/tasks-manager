from datetime import datetime
from app.base.base_pydantic import Base


class TokenResponse(Base):
    token_type: str = "Bearer"
    access_token: str


class AccessAndRefreshTokenResponse(Base):
    token_type: str = "Bearer"
    access_token: str
    refresh_token_in_cookie: bool


class ConfirmTokenResponse(Base):
    confirm_token: str


class RefreshTokenRequest(Base):
    refresh_token: str


class RefreshToken(Base):
    id: int
    token: str
    user_id: int
    created_at: datetime
    expire_at: datetime
    blocked: bool
