from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        index=True,
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
