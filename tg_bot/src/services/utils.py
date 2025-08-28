from typing import Any
from aiogram.types import CallbackQuery
from src.internal.api.models.base import Response
from aiogram.fsm.context import FSMContext
import json
from src.internal.redis.accessor import redis_api


def to_state_form(state_: str) -> str:
    return state_.replace("&", ":")


def to_callback_form(state_: str) -> str:
    return state_.replace(":", "&")


async def set_cache_in_state(state: FSMContext, update_data: Any):
    current_state = await state.get_state()
    data = await state.get_data()
    state_data: dict = data.get(current_state)
    cache_data = await get_cache_in_state(state)
    if cache_data is not None:
        cache_data.update(update_data)
    else:
        cache_data = update_data

    print("cache_data", cache_data)
    state_data["cache_data"] = cache_data

    await state.update_data(**{current_state: state_data})


async def get_cache_in_state(state: FSMContext) -> dict:
    current_state = await state.get_state()
    data = await state.get_data()
    state_data: dict = data.get(current_state)
    return None if not state_data.get("cache_data") else state_data.get("cache_data")


async def get_cache_page_in_state(state: FSMContext, page: int, project_id: int):
    current_state = await state.get_state()
    key = f"{state.key}:{project_id}"
    cache_data = await redis_api.get_page_data(key, current_state, page)
    if cache_data:
        return json.loads(cache_data)
    return None


async def set_cache_page_in_state(
    state: FSMContext, page: int, project_id: int, update_data: Any
):
    current_state = await state.get_state()
    update_data_json = json.dumps(update_data, default=str)
    key = f"{state.key}:{project_id}"
    await redis_api.set_page_data(key, current_state, page, update_data_json)


# async def answer_error(
#     callback: CallbackQuery, resp: Response, page: int, offset: int, state: str
# ):
#     if resp.status == 404:
#         nav_builder = get_page_keyboard(
#             offset=offset, page=page, limited=True, state=state
#         )
#         back_builder.attach(nav_builder)
#         await callback.message.edit_text(
#             "Тут пусто...", reply_markup=back_builder.as_markup()
#         )
#     else:
#         await callback.message.edit_text("Ошибка авторизации!!")
