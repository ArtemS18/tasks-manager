from typing import List
import typing
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, ForeignKey, Text

from app.auth.models.users import User
from app.base.base_model import Base
from app.lib.db import relationship

if typing.TYPE_CHECKING:
    from app.projects.models.member import Member
    from app.projects.models.tasks import Task


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    owner: Mapped["User"] = relationship("User")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")
    members: Mapped[List["Member"]] = relationship("Member", back_populates="project")
