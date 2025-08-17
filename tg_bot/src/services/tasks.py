from typing import Any, Dict
from aiogram.types import CallbackQuery
from src.bot.models.enums import PRIORITY_EMOJI, STATUS_BAR
from src.internal.api.models.dto import MessageDTO
from src.bot.models.states import UserBrowse
from src.bot.models import callbacks
from src.config import config
from aiogram.fsm.context import FSMContext
from src.keyboards import menu
from src.internal.api.models.tasks import TaskResponseSchema, Tasks, TasksResponseSchema
from src.internal.api.models.filters import TaskFilters
from src.internal.api.accessor import api
from src.services import utils


async def get_first_task_page(callback: CallbackQuery, state: FSMContext):
    callback_data = callbacks.TasksMenuCallback.unpack(callback.data)
    project_id = callback_data.project_id
    filter_data = callback_data.filter
    filters = TaskFilters(offset=0, limit=config.page_limit, project_id=project_id)

    if filter_data == "author":
        current_state = UserBrowse.my_tasks_author
        filters.is_author = True
    elif filter_data == "assign":
        current_state = UserBrowse.my_tasks_assign
        filters.is_assigned = True

    await state.set_state(current_state)
    data = await state.get_data()
    state_data: dict = data.get(current_state.state, {})
    state_data.update({"filters": filters.model_dump(), "fetch": "get_task_page"})
    dt = {current_state.state: state_data}

    await state.update_data(**dt)
    tasks_kb = await get_task_page(callback, filters.model_dump(), page=1, state=state)
    return tasks_kb


async def get_task_page(
    callback: CallbackQuery, _filters: Dict, page: int, state: FSMContext
):
    filters = TaskFilters(**_filters)
    current_state = await state.get_state()
    cache = await utils.get_cache_page_in_state(state, page, filters.project_id)
    print("current_state", current_state)
    back_builder = menu.get_back_btn(
        callbacks.ProjectCallback(id=filters.project_id).pack()
    )
    if not cache or cache == "null":
        resp = await api.fetch_tasks(callback.from_user.id, filters)
        if not resp.ok:
            if resp.status == 404:
                nav_builder = menu.get_page_keyboard(
                    offset=filters.offset,
                    page=page,
                    limited=True,
                    state=current_state,
                )
                nav_builder.attach(back_builder)
                return MessageDTO(
                    text="Тут пусто...", reply_markup=nav_builder.as_markup()
                )
            return MessageDTO(text="Ошибка")
        data: Tasks = resp.data
        dict_data = data.model_copy()

        await utils.set_cache_page_in_state(
            state, page, filters.project_id, dict_data.model_dump()
        )

    else:
        data = Tasks.model_validate(cache)
        print("Cached: ")

    limited = False
    if len(data.tasks) < config.page_limit:
        limited = True
    nav_builder = menu.get_page_keyboard(
        offset=filters.offset, limited=limited, page=page, state=await state.get_state()
    )
    task_builder = menu.get_tasks_keyboards(data.tasks)

    task_builder.attach(nav_builder)
    task_builder.attach(back_builder)
    return MessageDTO(text="Задачи: ", reply_markup=task_builder.as_markup())
    # await callback.message.edit_text("Задачи: ", reply_markup=task_builder.as_markup())


async def get_task_details(task_id: int, state: FSMContext):
    current_state = await state.get_state()
    resp = await api.fetch_task(task_id)
    back_builder = menu.get_back_btn(
        callbacks.PageCallback(
            action="prev", state=utils.to_callback_form(current_state)
        ).pack()
    )
    if not resp.ok:
        if resp.status == 404:
            return MessageDTO(text="Тут пусто...", reply_markup=back_builder)
        return MessageDTO(text="Ошибка")
    task: TaskResponseSchema = resp.data
    deadline = (
        "Нет" if task.deadline is None else f"{task.deadline.strftime('%d.%m.%Y')}"
    )
    text = (
        f"<b>Задача</b> {task.text}\n\n"
        f"<b>Автор</b>: \n - {task.author.name} \n - {task.author.login}\n\n"
        f"<b>Приоритет</b>: {PRIORITY_EMOJI[task.priority] + task.priority}\n\n"
        f"<b>Статус выполнения </b>: {STATUS_BAR[task.status]}\n\n"
        f"<b>Дедлайн</b>: {deadline}\n\n"
        f"<u>Дата создания</u>: {task.created_at.strftime('%d.%m.%Y')}\n\n"
    )
    assigns_btn = menu.get_assign_btn(task)
    assigns_btn.attach(back_builder)
    return MessageDTO(text=text, reply_markup=assigns_btn.as_markup())
