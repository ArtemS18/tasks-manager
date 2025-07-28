from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.internal.api.accessor import send

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello its me")
    data = await send()
    await message.answer(data.__str__())
