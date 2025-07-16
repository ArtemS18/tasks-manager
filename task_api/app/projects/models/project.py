from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, ForeignKey, Text

from app.base.base_model import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
