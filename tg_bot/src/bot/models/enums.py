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
    TaskPriority.low.value: "🟢",
    TaskPriority.default.value: "🔵",
    TaskPriority.high.value: "🟠",
    TaskPriority.very_high.value: "🔴",
}

STATUS_BAR = {
    TaskStatus.created.value: "Создана",
    TaskStatus.in_progress.value: "В процессе выполнения",
    TaskStatus.pending.value: "В процессе сдачи",
    TaskStatus.closed.value: "Задача выполнена",
}
