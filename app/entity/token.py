from datetime import datetime
from app.entity.base import Base

class RefreshTokenDTO(Base):
    token: str
    expire: datetime

class RefreshToken(Base):
    id: int
    user_id: int
    token: str
    created_at: datetime
    expire_at: datetime
    blocked: bool
