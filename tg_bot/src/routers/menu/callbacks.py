import logging
from typing import Callable
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import F

from src.internal.api.models.dto import MessageDTO
from src.services import projects, tasks
from src.bot.models.states import UserBrowse
from src.keyboards.menu import (
    get_tasks_in_project_kb,
    get_back_btn,
    get_assigns_keyboard,
)
from src.bot.models.callbacks import (
    PageCallback,
    ProjectCallback,
    TaskCallback,
    TasksMenuCallback,
    AssignsInTask,
)
from src.internal.api.accessor import api
from src.services.utils import to_state_form
from src.internal.api.models.filters import BaseFilters, ProjectFilters, TaskFilters
from src.keyboards.menu import inline_menu_kd
from src.services import const


router = Router()

log = logging.getLogger(__name__)


@router.callback_query(TasksMenuCallback.filter())
async def handel_tasks(callback: CallbackQuery, state: FSMContext):
    msg = await tasks.get_first_task_page(callback, state)
    await callback.message.edit_text(msg.text, reply_markup=msg.reply_markup)
    await callback.answer("GoD!")


@router.callback_query(TaskCallback.filter())
async def handel_task_details(
    callback: CallbackQuery, callback_data: TaskCallback, state: FSMContext
):
    msg = await tasks.get_task_details(callback_data.id, state)
    await callback.message.edit_text(
        msg.text, reply_markup=msg.reply_markup, parse_mode=ParseMode.HTML
    )
    await callback.answer("GoD!")


@router.callback_query(PageCallback.filter())
async def handle_page(
    callback: CallbackQuery, callback_data: PageCallback, state: FSMContext
):
    data = await state.get_data()
    current_state = to_state_form(callback_data.state)
    log.info(f"State {current_state}")
    state_data: dict = data.get(current_state)
    log.info(state_data)
    if state_data is None or current_state is None:
        await state.set_state(UserBrowse.menu)
        await callback.message.edit_text("Меню: ", reply_markup=inline_menu_kd)
        await callback.answer("Not found")
        return
    await state.set_state(current_state)
    filters: dict = state_data.get("filters")
    fetch: Callable = const.HANDEL_PAGE_CALLBACKS[state_data.get("fetch")]

    filters["offset"] = callback_data.offset
    page = callback_data.page

    msg: MessageDTO = await fetch(
        callback=callback, _filters=filters, page=page, state=state
    )
    await callback.message.edit_text(text=msg.text, reply_markup=msg.reply_markup)
    await callback.answer("GoD!")


@router.callback_query(lambda c: c.data == "my-projects")
async def handel_projects(callback: CallbackQuery, state: FSMContext):
    msg = await projects.get_first_project_page(callback, state)
    await callback.message.edit_text(msg.text, reply_markup=msg.reply_markup)
    await callback.answer()


@router.callback_query(ProjectCallback.filter())
async def handel_task_menu(
    callback: CallbackQuery, callback_data: ProjectCallback, state: FSMContext
):
    project_id = callback_data.id
    current_state = UserBrowse.my_tasks_menu

    await state.set_state(current_state)
    state_data = {current_state.state: {"project_id": project_id}}
    await state.update_data(**state_data)
    task_menu_builder = get_tasks_in_project_kb(project_id)
    task_menu_builder.attach(get_back_btn(back_callback_data="my-projects"))

    await callback.message.edit_text(
        "Задачи проекта:", reply_markup=task_menu_builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AssignsInTask.filter())
async def handel_assigns_int_task(
    callback: CallbackQuery, callback_data: AssignsInTask, state: FSMContext
):
    task = await api.fetch_task(callback_data.task_id)
    assigns_kb = get_assigns_keyboard(task.data)
    await callback.message.edit_text(
        "Участники задачи:", reply_markup=assigns_kb.as_markup()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "my-menu")
async def handel_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserBrowse.menu)
    await callback.message.edit_text("Меню: ", reply_markup=inline_menu_kd)
    await callback.answer()
