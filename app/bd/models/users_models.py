from datetime import datetime, time, timezone
from  sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, BigInteger, ForeignKey, DateTime, Boolean, func

from app.bd.base.base_model import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    login: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255))

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(VARCHAR(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expire_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), nullable=False)
    blocked: Mapped[bool]=mapped_column(Boolean, default=False)





