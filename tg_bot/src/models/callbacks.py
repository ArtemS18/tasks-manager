from typing import Literal
from aiogram.filters.callback_data import CallbackData

from src.models.states import UserBrowse


class PageCallback(CallbackData, prefix="page"):
    page: int = 1
    offset: int = 0
    action: Literal["prev", "next"]
    state: str


class TasksMenuCallback(CallbackData, prefix="my-tasks"):
    project_id: int
    filter: Literal["author", "assign", "notify"]


class TaskCallback(CallbackData, prefix="task"):
    id: int


class ProjectCallback(CallbackData, prefix="project"):
    id: int


class BackCallback(CallbackData, prefix="back"):
    tupe_: Literal["task-menu", "my-projects"]
    state: str
    data: dict


class AssignsInTask(CallbackData, prefix="assigns_task"):
    task_id: int
