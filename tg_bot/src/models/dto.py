from dataclasses import dataclass
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


@dataclass
class MessageDTO:
    text: str
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None
