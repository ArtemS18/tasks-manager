from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from src.services.tasks import TaskService
from aiogram.fsm.context import FSMContext
from src.internal.api.accessor import api
from src.internal.redis.accessor import redis_api


class DIMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state: FSMContext | None = data.get("state")
        if isinstance(event, CallbackQuery) and state is not None:
            callback: CallbackQuery = event
            data["task_service"] = TaskService(
                callback=callback, redis=redis_api, api=api, fsm=state
            )
        return await handler(event, data)
