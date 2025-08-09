from app.base.base_pydantic import Base


class UpdateUserSchema(Base):
    tg_id: int
