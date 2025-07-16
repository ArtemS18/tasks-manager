from enum import Enum as PyEnym


class TaskStatus(PyEnym):
    created = "created"
    in_progress = "in_progress"
    pending = "pending"
    closed = "closed"


class MemberRole(PyEnym):
    member = "member"
    admin = "admin"
    owner = "owner"


class MemberStatus(PyEnym):
    active = "active"
    blocked = "blocked"
