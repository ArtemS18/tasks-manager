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


class UserStatus(PyEnym):
    active = "active"
    pending = "pending"
    blocked = "blocked"


PRIORITY_EMOJI = {
    TaskPriority.low: "🟢",
    TaskPriority.default: "🔵",
    TaskPriority.high: "🟠",
    TaskPriority.very_high: "🔴",
}

STATUS_BAR = {
    TaskStatus.created: "Создана",
    TaskStatus.in_progress: "В процессе выполнения",
    TaskStatus.pending: "В процессе сдачи",
    TaskStatus.closed: "Задача выполнена",
}
