from aiogram import Router
from aiogram.types import CallbackQuery
from src.models.user import User

from src.internal.api.accessor import api

router = Router()


@router.callback_query(lambda c: c.data == "success-autho")
async def callback_autho(callback: CallbackQuery):
    user_resp = await api.check_user(callback.from_user.id)
    if not user_resp.ok:
        await callback.message.answer("Ошибка авторизации!!")
        return
    user: User = user_resp.data
    await callback.message.answer(
        f"Вы успешно авторизовались в боте: \n Имя: {user.name} \n Почта: {user.login}"
    )

    await callback.answer()
