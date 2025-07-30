from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.internal.api.accessor import api

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello its me")
    tasks = await api.fetch_tasks(1)
    for task in tasks.tasks:
        await message.answer(
            f"Задача {task.text} \n Автор: \n {task.author.login} \n {task.author.name} \n Cоздана: {task.created_at.strftime('%m/%d/%Y')}"
        )
