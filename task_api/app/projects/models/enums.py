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


class TaskPriority(PyEnym):
    low = "low"
    default = "default"
    high = "high"
    very_high = "very_high"


class RolePermission(PyEnym):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"
    all_permissions = "all_permissions"
