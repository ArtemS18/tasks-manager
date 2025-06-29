from app.entity.base import Base
from app.store.bd.models.users_models import UserStatus


class User(Base):
    id: int
    tg_id: int
    name: str
    login: str
    hashed_password: str
    status: UserStatus