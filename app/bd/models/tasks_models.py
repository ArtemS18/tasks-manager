from  sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer, ForeignKey, Text

from app.bd.base.base_model import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(VARCHAR(63))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))







