from aiogram.types import CallbackQuery
from src.models.dto import MessageDTO
from src.models.states import UserBrowse
from src.models.filters import ProjectFilters
from src.bot.config import config
from src.keyboards.menu import (
    get_back_btn,
    get_projects_keyboards,
    get_page_keyboard,
)
from aiogram.fsm.context import FSMContext
from src.models.tasks import Projects
from src.internal.api.accessor import api


async def get_project_page(
    callback: CallbackQuery, filters: ProjectFilters, page: int, state: str
):
    resp = await api.fetch_projects(callback.from_user.id, filters)

    back_builder = get_back_btn(back_callback_data="my-menu")
    if not resp.ok:
        if resp.status == 404:
            nav_builder = get_page_keyboard(
                offset=filters.offset, page=page, limited=True, state=state
            )
            nav_builder.attach(back_builder)
            return MessageDTO(text="Тут пусто...", reply_markup=nav_builder.as_markup())
        return MessageDTO(text="Ошибка")
    data: Projects = resp.data

    limited = False
    if len(data.projects) < config.page_limit:
        limited = True
    project_builder = get_projects_keyboards(data.projects)
    nav_builder = get_page_keyboard(
        offset=filters.offset, limited=limited, page=page, state=state
    )
    project_builder.attach(nav_builder)
    project_builder.attach(back_builder)

    return MessageDTO(text="Проекты: ", reply_markup=project_builder.as_markup())


async def get_first_project_page(callback: CallbackQuery, state: FSMContext):
    filters = ProjectFilters(limit=config.page_limit)
    current_state = UserBrowse.my_projects

    await state.set_state(current_state)
    state_data = {current_state.state: {"filters": filters, "fetch": get_project_page}}
    await state.update_data(**state_data)

    project_page = await get_project_page(
        callback,
        ProjectFilters(limit=config.page_limit),
        page=1,
        state=current_state.state,
    )
    return project_page
