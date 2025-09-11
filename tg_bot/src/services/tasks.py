import json
from typing import Any, Dict
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


from src.bot.models.enums import PRIORITY_EMOJI, STATUS_BAR
from src.internal.api.models.dto import MessageDTO
from src.bot.models.states import UserBrowse
from src.bot.models import callbacks
from src.config import config
from src.keyboards import menu
from src.internal.api.models.tasks import TaskResponseSchema, Tasks
from src.internal.api.models.filters import TaskFilters
from src.internal.api.accessor import ApiAccessor
from src.internal.redis.accessor import RedisAccessor
from src.services import utils


class TaskService:
    def __init__(
        self,
        api: ApiAccessor,
        redis: RedisAccessor,
        callback: CallbackQuery,
        fsm: FSMContext,
    ):
        self.api = api
        self.fsm = fsm
        self.redis = redis

        self.callback = callback
        self.data = callback.data

    @property
    async def state(self):
        return await self.fsm.get_state()

    async def _get_cache_task_page_in_state(self, page: int, project_id: int):
        key = f"{self.fsm.key}:{project_id}"
        cache_data = await self.redis.get_page_data(key, self.state, page)
        if cache_data:
            return json.loads(cache_data)
        return None

    async def _set_cache_task_page_in_state(
        self, page: int, project_id: int, update_data: Any
    ):
        update_data_json = json.dumps(update_data, default=str)
        key = f"{self.fsm.key}:{project_id}"
        await self.redis.set_page_data(key, self.state, page, update_data_json)

    async def set_state_and_data(self, current_state: str, filters: TaskFilters):
        await self.fsm.set_state(current_state)
        data = await self.fsm.get_data()
        state_data: dict = data.get(current_state, {})
        state_data.update({"filters": filters.model_dump(), "fetch": "get_task_page"})
        dt = {current_state: state_data}
        await self.fsm.update_data(**dt)

    async def get_first_task_page(self) -> MessageDTO:
        callback_data = callbacks.TasksMenuCallback.unpack(self.data)
        project_id = callback_data.project_id
        filter_data = callback_data.filter

        filters = TaskFilters(offset=0, limit=config.page_limit, project_id=project_id)
        if filter_data == "author":
            new_state = UserBrowse.my_tasks_author
            filters.is_author = True
        elif filter_data == "assign":
            new_state = UserBrowse.my_tasks_assign
            filters.is_assigned = True

        await self.set_state_and_data(new_state.state, filters)

        msg = await self.get_task_page(
            filters.model_dump(),
            page=1,
        )
        return msg

    async def handel_error_page(
        self,
        status,
        back_btn: InlineKeyboardBuilder | None = None,
        nav_builder: InlineKeyboardBuilder | None = None,
    ):
        if status == 404:
            reply_markup = back_btn.as_markup()
            if nav_builder:
                nav_builder.attach(back_btn)
                reply_markup = nav_builder.as_markup()
            return MessageDTO(text="Тут пусто...", reply_markup=reply_markup)
        return MessageDTO(text="Ошибка")

    async def get_task_page(
        self,
        _filters: Dict,
        page: int,
    ):
        filters = TaskFilters(**_filters)

        back_builder = menu.get_back_btn(
            callbacks.ProjectCallback(id=filters.project_id).pack()
        )
        nav_builder = menu.get_page_keyboard(
            offset=filters.offset, limited=True, page=page, state=self.state
        )

        cache = await self._get_cache_task_page_in_state(page, filters.project_id)
        if not cache or cache == "null":
            resp = await self.api.fetch_tasks(self.callback.from_user.id, filters)
            if not resp.ok:
                return await self.handel_error_page(
                    resp.status, back_builder, nav_builder
                )
            data: Tasks = resp.data
            dict_data = data.model_copy()

            await self._set_cache_task_page_in_state(
                page, filters.project_id, dict_data.model_dump()
            )
        else:
            data = Tasks.model_validate(cache)
            print("Cached: ")

        limited = False
        if len(data.tasks) < config.page_limit:
            limited = True
        nav_builder = menu.get_page_keyboard(
            offset=filters.offset, limited=limited, page=page, state=self.state
        )
        task_builder = menu.get_tasks_keyboards(data.tasks)

        task_builder.attach(nav_builder)
        task_builder.attach(back_builder)
        return MessageDTO(text="Задачи: ", reply_markup=task_builder.as_markup())

    async def get_task_details(self, task_id: int):
        resp = await self.api.fetch_task(task_id)
        back_builder = menu.get_back_btn(
            callbacks.PageCallback(
                action="prev", state=utils.to_callback_form(self.state)
            ).pack()
        )
        if not resp.ok:
            return await self.handel_error_page(resp.status, back_builder)
        task: TaskResponseSchema = resp.data
        deadline = (
            "Нет" if task.deadline is None else f"{task.deadline.strftime('%d.%m.%Y')}"
        )
        text = (
            f"<b>Задача</b> {task.text}\n\n"
            f"<b>Автор</b>: \n - {task.author.name} \n - {task.author.login}\n\n"
            f"<b>Приоритет</b>: {PRIORITY_EMOJI[task.priority] + task.priority}\n\n"
            f"<b>Статус выполнения </b>: {STATUS_BAR[task.status]}\n\n"
            f"<b>Дедлайн</b>: {deadline}\n\n"
            f"<u>Дата создания</u>: {task.created_at.strftime('%d.%m.%Y')}\n\n"
        )
        assigns_btn = menu.get_assign_btn(task)
        assigns_btn.attach(back_builder)
        return MessageDTO(text=text, reply_markup=assigns_btn.as_markup())
