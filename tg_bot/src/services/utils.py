from aiogram.types import CallbackQuery
from src.models.base import Response


def to_state_form(state_: str) -> str:
    return state_.replace("&", ":")


def to_callback_form(state_: str) -> str:
    return state_.replace(":", "&")


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
