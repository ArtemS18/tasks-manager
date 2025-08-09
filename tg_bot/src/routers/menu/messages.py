from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.models.states import UserBrowse
from src.keyboards.menu import inline_menu_kd
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    await state.set_state(UserBrowse.menu)
    await message.answer("Меню: ", reply_markup=inline_menu_kd)
