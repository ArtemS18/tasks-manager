from aiogram.types import CallbackQuery
from src.internal.api.models.dto import MessageDTO
from src.bot.models.states import UserBrowse
from src.internal.api.models.filters import ProjectFilters
from src.config import config
from src.keyboards.menu import (
    get_back_btn,
    get_projects_keyboards,
    get_page_keyboard,
)
from aiogram.fsm.context import FSMContext
from src.internal.api.models.tasks import Projects
from src.internal.api.accessor import api


async def get_project_page(
    callback: CallbackQuery, _filters: dict, page: int, state: FSMContext
):
    state = await state.get_state()
    filters = ProjectFilters(**_filters)
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
    data = await state.get_data()
    state_data: dict = data.get(current_state.state, {})
    state_data.update({"filters": filters.model_dump(), "fetch": "get_project_page"})
    dt = {current_state.state: state_data}

    await state.update_data(**dt)

    project_page = await get_project_page(
        callback,
        ProjectFilters(limit=config.page_limit).model_dump(),
        page=1,
        state=state,
    )
    return project_page
