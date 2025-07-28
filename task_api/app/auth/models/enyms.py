from enum import Enum as PyEnum


class UserStatus(PyEnum):
    active = "active"
    pending = "pending"
    blocked = "blocked"
