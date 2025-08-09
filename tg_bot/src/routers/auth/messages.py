from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from src.bot.config import config
from src.keyboards.autho import inline_auth_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Это бот для работы с задачами пропиши /login чтобы привязать этот тг аккаунт к своему профилю на сайте."
    )


@router.message(Command("login"))
async def login(message: Message):
    url = f"{config.site.url}?tg_id={message.from_user.id}"
    await message.answer(
        f"🔐 Авторизируйтесь на сайте чтобы привязать бота к аккаунту:\n{url}\n\nПосле этого нажмите кнопку ниже 👇",
        reply_markup=inline_auth_kb,
    )
