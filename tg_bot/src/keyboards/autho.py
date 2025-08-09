from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_auth_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Проверить", callback_data="success-autho")],
    ]
)
