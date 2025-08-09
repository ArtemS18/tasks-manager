from typing import Any, Literal
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.services.utils import to_callback_form
from src.models.enums import PRIORITY_EMOJI
from src.bot.config import config
from src.models.tasks import Project, TaskResponseSchema
from src.models import callbacks

inline_menu_kd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои проекты", callback_data="my-projects")],
        [InlineKeyboardButton(text="Уведомления", callback_data="my-notify")],
    ]
)


inline_task_kd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задачи", callback_data="my-tasks-assign")],
        [InlineKeyboardButton(text="Мои поручения", callback_data="my-tasks-author")],
        [InlineKeyboardButton(text="Уведомления", callback_data="my-notify")],
    ]
)


def get_tasks_in_project_kb(project_id: int):
    builder = InlineKeyboardBuilder()
    tasks_keyboards = [
        InlineKeyboardButton(
            text="Мои задачи",
            callback_data=callbacks.TasksMenuCallback(
                project_id=project_id, filter="author"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Мои поручения",
            callback_data=callbacks.TasksMenuCallback(
                project_id=project_id, filter="assign"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Уведомления",
            callback_data=callbacks.TasksMenuCallback(
                project_id=project_id, filter="notify"
            ).pack(),
        ),
    ]
    builder.add(*tasks_keyboards)
    builder.adjust(1)
    return builder


def get_assigns_keyboard(task: TaskResponseSchema):
    builder = InlineKeyboardBuilder()
    buttons = []
    for assign in task.assigns:
        buttons.append(
            InlineKeyboardButton(text=f"{assign.name}", callback_data="noop")
        )
    if buttons:
        builder.add(*buttons)
    builder.attach(get_back_btn(callbacks.TaskCallback(id=task.id).pack()))
    builder.adjust(1)
    return builder


def get_assign_btn(task: TaskResponseSchema):
    builder = InlineKeyboardBuilder()
    btn = [
        InlineKeyboardButton(
            text=f"Выполняющие эту задачу ({len(task.assigns)} учатников)",
            callback_data=callbacks.AssignsInTask(task_id=task.id).pack(),
        )
    ]
    builder.add(*btn)
    return builder


def get_back_btn(back_callback_data: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⏪Назад", callback_data=back_callback_data))
    return builder


def get_page_number_keyboard(page: int = 1):
    btn = [InlineKeyboardButton(text=f"стр. № {page}", callback_data="noop")]
    return btn


def get_page_keyboard(
    page: int, offset: int, limited: bool = False, state: str = ""
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    nav_buttons = []
    state = to_callback_form(state)

    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=callbacks.PageCallback(
                    page=page - 1,
                    offset=offset - config.page_limit,
                    action="prev",
                    state=state,
                ).pack(),
            )
        )

    if not limited:
        nav_buttons.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=callbacks.PageCallback(
                    page=page + 1,
                    offset=offset + config.page_limit,
                    action="next",
                    state=state,
                ).pack(),
            )
        )

    if len(nav_buttons) == 2:
        page_btn = get_page_number_keyboard(page)[0]
        nav_buttons.insert(1, page_btn)
    builder.add(*nav_buttons)

    return builder


def get_tasks_keyboards(tasks: list[TaskResponseSchema]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for task in tasks:
        priority = PRIORITY_EMOJI[task.priority]
        text = f"{priority} {task.id}) {task.text}"
        if task.deadline:
            text += f" сделать до: {task.deadline.strftime('%d.%m.%Y')}"
        else:
            text += " бессрочно."
        builder.button(
            text=text,
            callback_data=callbacks.TaskCallback(id=task.id).pack(),
        )
    builder.adjust(1)
    return builder


def get_projects_keyboards(projects: list[Project]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for project in projects:
        text = f" {project.id}) {project.name}"
        builder.button(
            text=text,
            callback_data=callbacks.ProjectCallback(id=project.id).pack(),
        )
    builder.adjust(1)
    return builder
