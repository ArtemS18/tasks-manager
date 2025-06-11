from  sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer

from app.bd.base.base_model import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, index=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    login: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255))





